# CI-PIPELINE.md

## CI Pipeline

### Goals
- [x] GitHub Actions workflow: static binary build, conformance gates, integration tests
- [x] lint-skill.sh: mechanical conformance gates G1-G8
- [x] Integration tests from VOCABULARY.md should/must-not-match cases

### Success Criteria
- Workflow passes on push to main
- Static binary produced (musl, linux-amd64)
- All G1-G8 mechanical gates pass
- All VOCABULARY.md test cases pass (should match / must not match)

### Notes
Build runs in the no-phase-skill submodule. Three jobs: build, conformance, test.
