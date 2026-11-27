#!/usr/bin/env python3
"""The plan/0113 harness probes: the pin, the arm loads, and the isolation checks.

The pinned binary is `.prefix/opencode`, installed by `install.sh`. Each check
builds a scratch root under `/tmp/opencode/plan0113/probes/` (outside any tree
that carries a manual), starts the pinned binary's server in that root, reads
the resolved surfaces through the public API, and kills the server. The
isolation check also runs a leak control: the same planted skill and manual in a
decoy home, once with that home as HOME (they load) and once with the draw's
scratch HOME (they do not exist for the draw).
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = HERE.parent / "arms"
BIN = HERE / ".prefix" / "opencode"
PREFLIGHT = HERE / "preflight.sh"
SCRATCH = Path(os.environ.get("PLAN0113_SCRATCH", "/tmp/opencode/plan0113/probes"))
BASE_PATH = "/usr/local/bin:/usr/bin:/bin"

PASSES: list[str] = []


class ProbeFailure(Exception):
    pass


def fail(message: str) -> None:
    raise ProbeFailure(message)


def note(message: str) -> None:
    PASSES.append(message)
    print(f"PASS {message}", flush=True)


def fresh(name: str) -> Path:
    root = SCRATCH / name
    if root.exists():
        shutil.rmtree(root)
    for part in ("home", "config", "data", "cache", "state", "work"):
        (root / part).mkdir(parents=True, exist_ok=True)
    return root


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


class Server:
    """One isolated `opencode serve` on a fresh root."""

    def __init__(self, root: Path, work: Path, home: Path, xdg: bool):
        self.root = root
        self.work = work
        self.home = home
        self.xdg = xdg
        self.process: subprocess.Popen[bytes] | None = None
        self.base: str | None = None
        self.auth: str | None = None
        self.serve_log = root / "serve.log"
        self.data_log = (
            (root / "data" / "opencode" / "log" / "opencode.log")
            if xdg
            else (home / ".local" / "share" / "opencode" / "log" / "opencode.log")
        )

    @classmethod
    def isolated(cls, root: Path) -> "Server":
        return cls(root, root / "work", root / "home", True)

    def environment(self) -> dict[str, str]:
        env = {
            "HOME": str(self.home),
            "PATH": BASE_PATH,
            "OPENCODE_DISABLE_AUTOUPDATE": "1",
            "OPENCODE_DISABLE_MODELS_FETCH": "1",
        }
        if self.xdg:
            env.update(
                {
                    "XDG_CONFIG_HOME": str(self.root / "config"),
                    "XDG_DATA_HOME": str(self.root / "data"),
                    "XDG_CACHE_HOME": str(self.root / "cache"),
                    "XDG_STATE_HOME": str(self.root / "state"),
                }
            )
        return env

    def __enter__(self) -> "Server":
        if not BIN.is_file():
            fail(f"the pinned binary is absent: {BIN} (run install.sh)")
        self.serve_log.unlink(missing_ok=True)
        self.process = subprocess.Popen(
            [str(BIN), "serve", "--hostname", "127.0.0.1", "--port", "0"],
            cwd=self.work,
            env=self.environment(),
            stdout=self.serve_log.open("wb"),
            stderr=subprocess.STDOUT,
        )
        deadline = time.time() + 20
        while time.time() < deadline:
            text = self.serve_log.read_text(errors="replace") if self.serve_log.exists() else ""
            if "server listening on " in text and "server password " in text:
                url = next(line for line in text.splitlines() if line.startswith("server listening on ")).split()[-1]
                password = next(line for line in text.splitlines() if line.startswith("server password ")).split()[-1]
                self.base = url.rstrip("/")
                self.auth = "Basic " + base64.b64encode(f"opencode:{password}".encode()).decode()
                self.await_surfaces()
                return self
            if self.process.poll() is not None:
                fail(f"the server exited before listening:\n{text}")
            time.sleep(0.1)
        fail("the server did not listen within 20s")

    def __exit__(self, *_: object) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=10)

    def get(self, path: str) -> object:
        assert self.base is not None and self.auth is not None
        request = urllib.request.Request(
            self.base + path,
            headers={
                "Authorization": self.auth,
                "x-opencode-directory": urllib.parse.quote(str(self.work), safe=""),
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.load(response)

    def data(self, path: str) -> list[dict]:
        payload = self.get(path)
        return payload.get("data", []) if isinstance(payload, dict) else []

    def ids(self, path: str) -> list[str]:
        return [item.get("id", "") for item in self.data(path)]

    def log_text(self) -> str:
        return self.data_log.read_text(errors="replace") if self.data_log.exists() else ""

    def await_surfaces(self) -> None:
        # Built-in plugins and skills activate asynchronously after the listener
        # starts. Wait until the surfaces settle before any check reads them.
        deadline = time.time() + 45
        while time.time() < deadline:
            try:
                plugins = self.ids("/api/plugin")
                skills = self.ids("/api/skill")
            except Exception:
                time.sleep(0.2)
                continue
            if "opencode.config.skill" in plugins and "opencode" in skills:
                time.sleep(0.5)
                return
            time.sleep(0.2)
        fail("the built-in surfaces did not activate within 45s")

    def await_log(self, needle: str, timeout: float = 15) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if needle in self.log_text():
                return True
            time.sleep(0.2)
        return False


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, timeout=120)


def check_pin() -> None:
    good = run([str(PREFLIGHT)])
    if good.returncode != 0:
        fail(f"preflight rejected the pinned binary: {good.stderr.strip()}")
    note(f"pin: {good.stdout.strip()}")

    tampered = SCRATCH / "tampered-opencode"
    shutil.copyfile(BIN, tampered)
    tampered.chmod(0o755)
    with tampered.open("ab") as handle:
        handle.write(b"\0")
    wrong_digest = run([str(PREFLIGHT), "--bin", str(tampered), "--check", "digest"])
    if wrong_digest.returncode == 0 or "REJECT digest" not in wrong_digest.stderr:
        fail(f"preflight did not reject a tampered digest: rc={wrong_digest.returncode} {wrong_digest.stderr}")
    note("pin: preflight rejects a wrong digest")

    fake_version = SCRATCH / "fake-version-opencode"
    write(fake_version, "#!/bin/sh\necho 'opencode v9.9.9'\n")
    fake_version.chmod(0o755)
    wrong_version = run([str(PREFLIGHT), "--bin", str(fake_version), "--check", "version"])
    if wrong_version.returncode == 0 or "REJECT version" not in wrong_version.stderr:
        fail(f"preflight did not reject a wrong version: rc={wrong_version.returncode} {wrong_version.stderr}")
    note("pin: preflight rejects a wrong version")

    both = run([str(PREFLIGHT), "--bin", str(tampered)])
    if both.returncode == 0:
        fail("preflight accepted a tampered binary under the default check")
    note("pin: preflight rejects a tampered binary under the default check")


def builtin_baseline(server: Server) -> tuple[list[str], list[str], list[str]]:
    plugins = server.ids("/api/plugin")
    skills = server.ids("/api/skill")
    agents = server.ids("/api/agent")
    foreign_plugins = [item for item in plugins if not item.startswith("opencode.")]
    if foreign_plugins:
        fail(f"the null draw loaded a foreign plugin: {foreign_plugins}")
    return plugins, skills, agents


def check_null(
    builtin_plugins: list[str], builtin_skills: list[str], builtin_agents: list[str]
) -> None:
    root = fresh("null")
    with Server.isolated(root) as server:
        plugins, skills, agents = builtin_baseline(server)
        if sorted(plugins) != sorted(builtin_plugins):
            fail(f"the null draw's plugin set differs from the baseline: {plugins}")
        if sorted(skills) != sorted(builtin_skills):
            fail(f"the null draw's skill set differs from the baseline: {skills}")
        if sorted(agents) != sorted(builtin_agents):
            fail("the null draw's agent set differs from the baseline")
        entries = server.get("/api/config")
        assert isinstance(entries, list)
        for entry in entries:
            if entry.get("type") != "directory":
                fail(f"the null draw resolved a config document: {entry}")
            info = entry.get("info") or {}
            for key in ("skills", "plugins", "instructions"):
                if key in info:
                    fail(f"the null draw's config carries {key}: {info[key]}")
        if any(root.rglob("AGENTS.md")):
            fail("the null draw's scratch tree carries a manual")
        note(
            "null: resolved config lists no skill, plugin or instruction; "
            f"catalog is the binary's built-ins only (skills: {', '.join(skills)})"
        )


def plant_skills(root: Path, sources: list[tuple[Path, str]]) -> None:
    for source, name in sources:
        destination = root / "config" / "opencode" / "skills" / name
        shutil.copytree(source, destination)


def plant_agents(root: Path, sources: list[tuple[Path, str]]) -> None:
    for source, relative in sources:
        destination = root / "config" / "opencode" / "agents" / relative
        write(destination, source.read_text())


def check_skill_arm(
    name: str,
    skills: list[tuple[Path, str]],
    expected_skills: list[str],
    builtin_skills: list[str],
    builtin_agents: list[str],
    agents: list[tuple[Path, str]] | None = None,
    expected_agents: list[str] | None = None,
) -> None:
    root = fresh(name)
    plant_skills(root, skills)
    if agents:
        plant_agents(root, agents)
    with Server.isolated(root) as server:
        deadline = time.time() + 30
        while time.time() < deadline:
            loaded = server.ids("/api/skill")
            if all(item in loaded for item in expected_skills):
                break
            time.sleep(0.2)
        else:
            fail(f"{name}: the expected skills did not load: {expected_skills}; got {server.ids('/api/skill')}")
        extra_skills = sorted(set(loaded) - set(builtin_skills))
        if extra_skills != sorted(expected_skills):
            fail(f"{name}: foreign skills leaked into the arm root: {extra_skills}")
        loaded_agents = server.ids("/api/agent")
        if expected_agents:
            extra_agents = sorted(set(loaded_agents) - set(builtin_agents))
            if extra_agents != sorted(expected_agents):
                fail(f"{name}: foreign agents leaked into the arm root: {extra_agents}")
        note(
            f"{name}: loaded under the pinned binary "
            f"(skills: {', '.join(expected_skills)}"
            + (f"; agents: {', '.join(expected_agents)}" if expected_agents else "")
            + ")"
        )


def check_hffmnnj(builtin_skills: list[str], builtin_agents: list[str]) -> None:
    root = fresh("hffmnnj")
    config = root / "config" / "opencode" / "opencode.json"
    write(config, json.dumps({"plugins": [f"file://{ARMS / 'hffmnnj'}"]}, indent=2) + "\n")
    with Server.isolated(root) as server:
        deadline = time.time() + 60
        while time.time() < deadline:
            if "hffmnnj.deep-research" in server.ids("/api/plugin"):
                break
            time.sleep(0.2)
        else:
            fail("hffmnnj: the plugin did not load under the pinned binary")
        foreign_plugins = [item for item in server.ids("/api/plugin") if not item.startswith("opencode.")]
        if foreign_plugins != ["hffmnnj.deep-research"]:
            fail(f"hffmnnj: foreign plugins leaked into the arm root: {foreign_plugins}")
        extra_skills = sorted(set(server.ids("/api/skill")) - set(builtin_skills))
        if extra_skills != ["deep-research"]:
            fail(f"hffmnnj: the plugin loaded without its skill: {extra_skills}")
        extra_agents = sorted(set(server.ids("/api/agent")) - set(builtin_agents))
        expected = ["deep-research/librarian", "deep-research/researcher", "deep-research/verifier"]
        if extra_agents != expected:
            fail(f"hffmnnj: the plugin loaded without its agents: {extra_agents}")
        note("hffmnnj: plugin, skill and three agents loaded under the pinned binary")


def check_isolation() -> None:
    decoy = SCRATCH / "isolation" / "decoy"
    if decoy.exists():
        shutil.rmtree(decoy)
    home = decoy / "home"
    write(
        home / ".config" / "opencode" / "skills" / "planted-native" / "SKILL.md",
        "---\nname: planted-native\ndescription: A skill planted in the host home.\n---\n# planted\n",
    )
    write(
        home / ".claude" / "skills" / "planted-claude" / "SKILL.md",
        "---\nname: planted-claude\ndescription: A Claude skill planted in the host home.\n---\n# planted\n",
    )
    write(
        home / ".agents" / "skills" / "planted-agents" / "SKILL.md",
        "---\nname: planted-agents\ndescription: An agents skill planted in the host home.\n---\n# planted\n",
    )
    write(home / ".config" / "opencode" / "AGENTS.md", "# Planted global manual\n\nThis manual must not reach a draw.\n")
    write(home / "AGENTS.md", "# Planted project manual\n\nThis manual must not reach a draw.\n")
    (home / "work").mkdir(parents=True, exist_ok=True)

    leak = Server(decoy, home / "work", home, False)
    with leak:
        skills = leak.ids("/api/skill")
        if "planted-native" not in skills:
            fail(f"the leak control did not load the planted skill: {skills}")
        global_manual = home / ".config" / "opencode" / "AGENTS.md"
        project_manual = home / "AGENTS.md"
        if not leak.await_log(str(global_manual)) and not leak.await_log(str(project_manual)):
            fail("the leak control did not discover a planted manual")
        note("isolation: leak control loads the planted skill and discovers the planted manual")

    draw = fresh("isolation/draw")
    with Server.isolated(draw) as server:
        skills = server.ids("/api/skill")
        if "planted-native" in skills or "planted-claude" in skills or "planted-agents" in skills:
            fail(f"the draw loaded a skill planted in the host home: {skills}")
        log = server.log_text()
        for needle in (str(home), "Planted global manual", "Planted project manual"):
            if needle in log:
                fail(f"the draw's log references the host home: {needle}")
        note("isolation: the planted skill and manual in the host home are absent from the draw")


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    check_pin()

    baseline_root = fresh("baseline")
    with Server.isolated(baseline_root) as baseline:
        builtin_plugins, builtin_skills, builtin_agents = builtin_baseline(baseline)
    check_null(builtin_plugins, builtin_skills, builtin_agents)

    weizhena_skills = [
        (ARMS / "weizhena" / "skills" / "research-en" / "research", "research"),
        (ARMS / "weizhena" / "skills" / "research-en" / "research-deep", "research-deep"),
        (ARMS / "weizhena" / "skills" / "research-en" / "research-report", "research-report"),
        (ARMS / "weizhena" / "skills" / "research-en" / "research-add-items", "research-add-items"),
        (ARMS / "weizhena" / "skills" / "research-en" / "research-add-fields", "research-add-fields"),
    ]
    check_skill_arm(
        "weizhena",
        weizhena_skills,
        [name for _, name in weizhena_skills],
        builtin_skills,
        builtin_agents,
        agents=[(ARMS / "weizhena" / "agents" / "web-search-opencode.md", "web-search.md")],
        expected_agents=["web-search"],
    )
    check_skill_arm(
        "kanatami",
        [(ARMS / "kanatami", "web-search-deep")],
        ["web-search-deep"],
        builtin_skills,
        builtin_agents,
        agents=[(ARMS / "kanatami" / "agents" / "web-search-worker.md", "web-search-worker.md")],
        expected_agents=["web-search-worker"],
    )
    check_skill_arm(
        "samber",
        [(ARMS / "samber" / "skills" / "deep-research", "deep-research")],
        ["deep-research"],
        builtin_skills,
        builtin_agents,
    )
    check_hffmnnj(builtin_skills, builtin_agents)
    check_isolation()

    print(f"probe: {len(PASSES)} checks passed", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProbeFailure as error:
        print(f"FAIL {error}", file=sys.stderr, flush=True)
        raise SystemExit(1)
