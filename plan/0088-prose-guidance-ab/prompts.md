# The prompts, verbatim

Each condition's prompt is the task block followed by the guidance block (A has none). Tasks alternate per draw index.

## The task blocks

- **T1 (capability description)**: `Write a short passage (80-120 words) for a README describing a new capability of a command-line tool: the tool reconciles a project's manifest files against a template that has moved, proposing merges instead of overwriting. Do not invent features beyond this.`
- **T2 (milestone summary)**: `Write a short summary paragraph (80-120 words) for a project record, summarizing a milestone that migrated a repository from numbered folder names to names derived from each folder's contents, and gated the rename with a dictionary-driven checker.`

## The guidance blocks

- **A (control)**: none.
- **B (negative list)**: `Avoid these words and constructions: delve, tapestry, synergy, landscape, intricate, nuanced, multifaceted, realm, showcase, leverage (as a verb), harness (as a verb), framework (in the grandiose sense), deeply, fundamentally, remarkably, profoundly, crucially, "serves as", "stands as"; avoid em-dashes, arrows, and three-part parallel sentences.`
- **C (positive exemplars)**: `Write in the manner of these examples: "The checker reads every manifest, compares each against the template's current revision, and proposes a merge per drifted file. Nothing is overwritten without an explicit confirmation, and every proposal names the files it touched."`
