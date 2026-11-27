# plan/0113 task sets: the frozen selection set and the sealed held-out set

- Frozen 2026-11-27, before the first draw. The selection round is later, and
  nothing in this record was produced by a draw.
- The schema is `schema.py`. A task carries its key, kind and digest; a set
  carries a digest over its task list.
- `selection.json` is the selection set and is read by the selection round.
- `held-out.json.enc` is the held-out set, stored as ciphertext. Its plaintext
  was validated before sealing and deleted. `sets.json` carries its plaintext
  set digest and ciphertext digest.

## The benchmark

Known-answer tasks reference SimpleQA by row, not by embedding the question or
answer. The dataset is fetched at run time and checked against the frozen
digest, so the benchmark's own terms apply.

| Field | Value |
|---|---|
| Benchmark | SimpleQA, `openai/simple-evals` |
| Dataset | `https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv` |
| Dataset sha256 | `feee3f7e7db3617e94e8fcf1977b756ec420ef8568f4e0fcbbe0e92e9d5fc032` |
| Rows | 4326 |
| License | MIT |

A known-answer task's body is its key, kind, source (`benchmark`,
`dataset_url`, `dataset_sha256`, `row`) and its digest. It carries no
`question`; the selection harness resolves the row to the benchmark's question
and answer at draw time.

## The selection set

Six tasks: three known-answer rows and three house tasks.

| Key | Kind | The task |
|---|---|---|
| `selection/simpleqa-0000` | known-answer | SimpleQA row 0 |
| `selection/simpleqa-0002` | known-answer | SimpleQA row 2 |
| `selection/simpleqa-1000` | known-answer | SimpleQA row 1000 |
| `selection/house-path-crates` | house | `bstr` or `os_str_bytes` for non-UTF-8 path classification: byte-path type and license |
| `selection/house-rg-ast-grep` | house | ripgrep or ast-grep for a prose scan: language, license, query language and syntax-tree query |
| `selection/house-host-lint-docs` | house | which host-lint release added `--docs` and which rule source it consults |

The house tasks' must-cover lists are in `selection.json`: the candidates, the
byte-path type, the licenses, the query languages, the release version, the
flag and the rule source. Each entity carries its aliases.

The selection set digest is
`128d135446134687ef6249d9aa902863920bd63c3bdf0130e885e9ed19ede36e`.

## The held-out set

Five tasks: two known-answer rows and three house tasks. The plaintext set
digest is
`97c44bd2fef9ed2394104bf19e3f05bf43fc937f527db13b78604bd75d038888`;
the ciphertext digest is
`a8efb99765315c888ac5ad3a0cc7d799afdf173d8bce07d115f453e607b1d42c`.

The held-out task keys and questions are not in this record. They are in the
ciphertext only. The freeze validated the plaintext before sealing: `ok
held-out: 5 tasks (2 known-answer, 3 house), digest
97c44bd2fef9ed2394104bf19e3f05bf43fc937f527db13b78604bd75d038888`. The
selection round reads `selection.json`; it does not read `held-out.json.enc` or
the key, and the selection harness records that constraint. The confirmation
round decrypts the file, validates the set and compares the recovered set
digest with `sets.json`.

## The seal

The held-out plaintext was written under `/tmp`, validated by
`schema.validate_set`, encrypted with:

```sh
openssl enc -aes-256-cbc -pbkdf2 -salt -in held-out.json -out held-out.json.enc -pass file:<key>
```

The key is a 32-byte hex string at `/tmp/opencode/plan0113/held-out.key`, mode
600, outside the repository, and the plaintext was deleted. The operator should
move the key to their own custody. The selection round must not read it; that
is the protocol's rule, and the mechanical part is the ciphertext with no
plaintext in the tree. The authoring script was a one-off under `/tmp` and is
not committed, because it carries the held-out task text.

## The checks

```sh
cd plan/0113-host-deep-research-ab/harness/tasks
python3 schema.py validate selection.json
python3 schema.py check selection.json held-out.json.enc sets.json
```

```
ok selection: 6 tasks (3 known-answer, 3 house), digest 128d135446134687ef6249d9aa902863920bd63c3bdf0130e885e9ed19ede36e
ok selection: 6 tasks, 3 known-answer, 3 house
ok selection digest: 128d135446134687ef6249d9aa902863920bd63c3bdf0130e885e9ed19ede36e
ok held-out: 5 tasks sealed, ciphertext a8efb99765315c888ac5ad3a0cc7d799afdf173d8bce07d115f453e607b1d42c
ok held-out plaintext digest recorded: 97c44bd2fef9ed2394104bf19e3f05bf43fc937f527db13b78604bd75d038888
ok frozen before the first draw (sets.json recorded before the selection round)
```

The check reads the selection set, validates every task's digest and the set
digest, matches the ciphertext digest, asserts the OpenSSL `Salted__` header,
and asserts no plaintext held-out file sits beside it. It does not decrypt the
held-out set.

At confirmation:

```sh
python3 schema.py decrypt held-out.json.enc <key> /tmp/held-out.json
python3 schema.py validate /tmp/held-out.json
```

The decrypted set's digest is compared with
`sets.json.held_out.plaintext_set_digest`.

## What is still open

The number of draws per task and the per-draw budget are the protocol's open
questions. The set sizes are fixed here at six selection tasks and five
held-out tasks; changing them after a draw would require a new freeze and a
recorded reason.
