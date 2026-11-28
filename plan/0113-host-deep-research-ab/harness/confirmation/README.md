# plan/0113 confirmation: the locked arm against null on fresh-2

The confirmation is the first read of the fresh-2 held-out set. It pits the arm
locked by `selection/round-redo.json` against `null` on five unseen tasks, two
fresh draws per task per arm, in a recorded random order within each task
block. The verdict is the frozen criteria, not a reviewer's impression.

## The seal

The first fresh set was decrypted by the old `--check`, so it is burned. The
fresh-2 set is authored outside the repository and sealed with an
operator-held key:

```sh
cd plan/0113-host-deep-research-ab/harness/tasks
python3 seal.py --set /tmp/fresh2/tasks.json --key /path/to/operator.key \
  --sealed held-out-fresh2.json.enc --sets sets-fresh2.json
```

`seal.py` validates the set, writes the ciphertext, records the plaintext and
ciphertext digests, and deletes the plaintext. It never creates a key. The
plaintext task text is never committed.

`--check` reads only the seal:

```sh
cd plan/0113-host-deep-research-ab/harness/confirmation
python3 confirm.py --check
```

It matches the ciphertext digest, asserts the OpenSSL `Salted__` header,
asserts no plaintext sits beside the ciphertext, and compares the recorded
selection digest. It does not take a key and does not decrypt.

## The run

```sh
python3 confirm.py --key /path/to/operator.key --parallel 2
```

The key is required and has no default path. The run decrypts the set to
memory, validates its digest against `sets-fresh2.json`, reads the locked arm
from `selection/round-redo.json` (never a hard-coded `weizhena`), and refuses an
existing draw directory without `--force`.

The execution order is shuffled per task block and recorded in `verdict.json`
with its seed. A harness break is re-run once under the same task and config;
the prior attempt stays under `attempts/` with `rerun.json`. A budget void and
an arm exclusion are terminal and are a gate, never a measured zero.

Every valid draw is judged with the pinned Opus 5.5 judge after the draws. The
judge's model, route and validity gate are checked; a missing or malformed
judge reply fails the `judge` criterion. The judge score is recorded, not part
of the 1.0-point mechanical margin.

## The verdict

`verdict.json` records the per-task and pooled mechanical scores, the margin,
the judge result and the criteria:

- `draws`: every draw is valid or has a recorded harness-break re-run.
- `margin`: the locked arm's pooled score is at least 1.0 point above `null`.
- `floor`: every locked-arm task mean is at least 8 of 16.
- `phantom`: zero phantom sources.
- `foreign`: no foreign-model receipt and every reply ledger passes.
- `judge`: every valid draw has a valid Opus 5.5 judge score.

`SHIP` means every criterion passes. `NO-SHIP` prints the missed criteria and
the incumbent (`null`) stands. The operator's `goal accept` is the milestone;
the verdict is evidence, not the acceptance.

## State

The fresh-2 set is not sealed yet: the operator holds the key and supplies the
plaintext set outside the repository. `seal.py`, `confirm.py --check` and the
in-memory decrypt path are tested against a temporary one-task set. The
selection round must lock an arm before the confirmation can run.
