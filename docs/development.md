# Development workflow

Use the pinned toolchain and the repository's `just` recipes. Keep runtime
credentials, private estate data and live telemetry outside this repository.

`main` and `dev` are permanent branches. Make scoped changes on a working
branch, submit a pull request to `dev`, and promote reviewed changes from
`dev` to `main`. Use Conventional Commits and signed commits. Do not delete
permanent branches or rewrite published history.

The `NDS checks / quality` job runs on GitHub-hosted Ubuntu with read-only
repository permissions and immutable action pins. It checks this repository's
current foundation. A green result is not deployment, release, integration or
cross-platform acceptance. Full release gates remain those in the locked
central standards.

## Standards compatibility

The module standards lock remains at `v0.0.1-alpha.7` (`592531d`).
Central `v0.0.1-alpha.8` (`c73a525`) changes assembly catalog metadata only;
the normative `standarts/` files are identical. The older lock is compatible
with the current assembly. Update locks only through the canonical source
release, not through a mutable branch.

The canonical NDDev mark in `assets/nddev-mark.svg` comes from the public
OpenNetwork header at https://nddev.ai/opennetwork/en; `brand-source.json`
records its reviewed geometry digest. Launcher colors remain existing design
tokens. This asset-only addition is compatible with the unchanged alpha.7 lock.

Install the pinned renderer with `python3 -m pip install --require-hashes -r
tools/requirements-icons.txt` in an isolated environment. From a committed DS
source, `python3 tools/generate_launchers.py --desktop /path/to/desktop --mobile
/path/to/mobile` renders required native images and records source/input/output
SHA-256 provenance. Byte generation and `--check` use the canonical Linux x86_64
renderer: CPython 3.14.4, Pillow 12.1.1 and its zlib 1.3.1 backend. Linux wheels
link the host zlib; `bash tools/with-renderer-zlib.sh <command>` builds the
checksum-pinned upstream backend in a temporary prefix for one command, then
removes that prefix. It does not replace system libraries. CI uses this wrapper
for generation checks. Other Pillow
wheels may encode identical pixels with different compression. Every target runs
`--verify` to check the committed asset inventory, bytes and immutable source/input/
renderer provenance without requiring Pillow. CI also retains strict Linux byte
regeneration. Do not copy or redraw the SVG in consumers. The renderer is a
development tool, not a runtime dependency.
