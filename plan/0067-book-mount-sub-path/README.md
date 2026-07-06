# plan/0067 book-mount-sub-path: publish the development book under a sub-path of an existing site

This milestone answers host#17. Some adopters already serve a content-full product site from their
Pages root, so the reference Site workflow, which publishes the generated book as the whole site, would
overwrite it. The fix makes the book's mount point a declared, machine-readable key rather than a
hand-authored workflow exception, so a product-site-at-root adopter needs configuration, not a durable
workaround the next template upgrade silently drops.

## The tool side (shipped in host-lifecycle v0.38.0)

The mount point is an optional flat `book-mount` key in the `.host` stamp, defaulting to `/`. It is read
through the existing stamp reader, so it needs no new parser and survives a baseline re-stamp.
`host-lifecycle book` emits mdBook's `[output.html] site-url` from it, and only for a non-default mount,
so `book.toml` stays byte-identical for every project that publishes at the root; a sub-path mount then
resolves the book's absolute links (the 404 and print pages) correctly. A `book --print-mount` mode
prints the normalized mount for the reference Site workflow to consume, so the workflow reads the value
from the tool rather than shell-parsing the stamp (the internalise-tool-orchestration doctrine). A unit
test covers both the default (no `site-url`) and a declared sub-path.

## The spine side (pending, ships with the template roll)

The reference Site workflow the template ships is made mount-aware: it publishes the book under the
declared sub-path with the surrounding site kept, and asserts the layout after the build. The publish
recheck in `lifecycle.manifest` points at the tool's mount-aware mode rather than testing a hardcoded
workflow filename, which also fixes a latent brittleness where the recheck named `mdbook.yml` while the
template ships `site.yml`. The `book-mount` key, its default, and the sub-path boundary are documented in
the spine, and an UPGRADING.md ledger entry keyed to that doctrine commit carries it to adopters, with a
`requires` on the host-lifecycle release above. This half lands in the template roll.

## Verification

Tool side: the unit test asserts a default mount emits no `site-url` and a declared sub-path emits it,
and `book --print-mount` returns the declared value; shipped reproducibly in host-lifecycle v0.38.0.
Spine side: a mount-aware Site workflow publishes the book under the sub-path without overwriting the
surrounding site, and the publish recheck passes against the tool's mode. Both land with the whole-suite
verify gate green.
