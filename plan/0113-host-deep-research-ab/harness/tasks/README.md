# plan/0113 task sets: the frozen selection set and the sealed held-out sets

**Status: the selection set stands; both earlier held-out sets are burned.**
The first held-out set was read at the failed confirmation. The fresh set was
then decrypted by the old `confirm.py --check`, so it is burned too. The
confirmation uses a fresh-2 set sealed with an operator-held key; `seal.py`
seals it and `confirm.py --check` reads only the ciphertext.

- Frozen 2026-11-27, before the first draw. The selection round is later, and
  nothing in this record was produced by a draw.
- The schema is `schema.py`. A task carries its key, kind and digest; a set
  carries a digest over its task list.
- `selection.json` is the selection set and is read by the selection round.
- `held-out.json.enc` and `held-out-fresh.json.enc` are burned. Their
  plaintexts were read at the failed confirmations. `sets.json` and
  `sets-fresh.json` stay as history.
- `held-out-fresh2.json.enc` and `sets-fresh2.json` are the confirmation's
  set. They are written by `seal.py` from an operator-supplied plaintext set
  and key.

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

## The burned held-out sets

The first held-out set carried five tasks (two known-answer, three house). Its
plaintext digest was
`97c44bd2fef9ed2394104bf19e3f05bf43fc937f527db13b78604bd75d038888`
and its ciphertext digest
`a8efb99765315c888ac5ad3a0cc7d799afdf173d8bce07d115f453e607b1d42c`.
The old confirmation read the plaintext, so it is history.

The fresh set carried five tasks (two known-answer, three house). Its plaintext
digest is
`9c40958960c58d6c1f3e9b2a3b9dcd0f407abe92659826b018f1ff74cadcb5be`
and its ciphertext digest
`bb60b746bddea73fac5c8a99ba70869d178da36c3cb7a5b5df4a7324b099b9c2`.
The old `confirm.py --check` decrypted it, so it is burned as well. Both
plaintext task texts are absent from the tree.

## The fresh-2 set

The confirmation set is authored outside the repository, validated by
`schema.validate_set`, and sealed with an operator-held key:

```sh
cd plan/0113-host-deep-research-ab/harness/tasks
python3 seal.py --set /tmp/fresh2/tasks.json --key /path/to/operator.key \
  --sealed held-out-fresh2.json.enc --sets sets-fresh2.json
```

`seal.py` refuses a plaintext set inside the repository, refuses to overwrite
an existing seal without `--force`, writes the ciphertext and the record, and
deletes the plaintext. It never creates a key. The plaintext task text is not
committed.

`sets-fresh2.json` records the selection digest, the benchmark, the plaintext
set digest, the ciphertext digest and the task counts. It records the key as
operator-held, not a path; the confirmation takes `--key` explicitly.

## The checks

```sh
cd plan/0113-host-deep-research-ab/harness/tasks
python3 schema.py validate selection.json
python3 schema.py check selection.json held-out.json.enc sets.json
```

The check reads the selection set, validates every task's digest and the set
digest, matches the ciphertext digest, asserts the OpenSSL `Salted__` header,
and asserts no plaintext held-out file sits beside it. It does not decrypt.

`confirm.py --check` is the fresh-2 equivalent:

```sh
cd plan/0113-host-deep-research-ab/harness/confirmation
python3 confirm.py --check
```

It does not take a key and does not write a plaintext. A run takes
`--key /path/to/operator.key`, decrypts to memory, and compares the recovered
set digest with `sets-fresh2.json.held_out.plaintext_set_digest`.

## What is still open

The fresh-2 set is sealed; its key is outside the repository and the
confirmation takes `--key` explicitly. The durable custody copy is the private
repo `connollydavid/plan0113-fresh2-key` (`fresh2.key`). The selection must lock an arm before
the 20 confirmation draws can run. The draw protocol is fixed at two fresh
draws per held-out task per arm.
