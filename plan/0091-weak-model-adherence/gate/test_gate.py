"""Tests for lemgate: scorer units and the enforce loop against a fake
upstream that violates on demand."""

import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

import lemgate


class ScorerTests(unittest.TestCase):
    def test_clean(self):
        self.assertFalse(score_of("L have gone ahead. Say go again whenever you are ready.")["violation"])

    def test_lemu_violation(self):
        s = score_of("lemu has the convention ready.")
        self.assertTrue(s["violation"])
        self.assertIn("lemu", s["lem_tokens"])

    def test_mangle_violation(self):
        s = score_of("whenever lemua says go")
        self.assertTrue(s["violation"])
        self.assertIn("lemua", s["mangles"])

    def test_third_person_lem_is_strict_violation(self):
        self.assertTrue(score_of("I gave lem the credentials.")["violation"])


def score_of(text):
    return lemgate.score(lemgate.strip_think(text)[0])


class _FakeUpstream(BaseHTTPRequestHandler):
    """Returns a violating reply once, then a clean one."""

    calls = 0

    def do_POST(self):  # noqa: N802
        _FakeUpstream.calls += 1
        if _FakeUpstream.calls % 2 == 1:
            content = "lemu has the convention ready for L's sign-off."
        else:
            content = "L has the convention ready for you."
        body = json.dumps({
            "choices": [{"finish_reason": "stop",
                         "message": {"content": content, "role": "assistant"}}],
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


class EnforceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        lemgate.UPSTREAM = f"http://127.0.0.1:{cls.server.server_port}"
        cls.body = {"model": "x", "messages": [{"role": "user", "content": "q"}]}

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_violation_is_rewritten(self):
        out, audit = lemgate.enforce(dict(self.body), "Bearer t")
        self.assertTrue(out["x-lemgate"]["clean"])
        self.assertEqual(out["x-lemgate"]["retries"], 1)
        self.assertEqual(len(audit), 2)
        self.assertIn("L has the convention", out["choices"][0]["message"]["content"])

    def test_off_mode_flag_shape(self):
        self.assertEqual(lemgate.MODE, "strict")


if __name__ == "__main__":
    unittest.main()
