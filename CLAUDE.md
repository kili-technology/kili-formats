<!--
    Review: 27/11/2026

    Rules for this file (Anthropic guidance):
    - keep it under 200 lines
    - `/doctor` trims anything Claude can derive from the code
    - every line must answer "would removing this make Claude get it wrong?"
    - no architecture summaries, no dependency lists, no file-by-file map (Claude reads those faster than we maintain them)
-->

# kili-formats

Label format conversions, published to PyPI as `kili-formats`.

## Gotchas

- **Merging ships nothing.** PyPI publishes when a GitHub Release is published (a pre-release does not trigger it), and it uploads the version written in `pyproject.toml`, bumped by hand — the tag name is never read. kili-python-sdk and export pin an exact version, so a release reaches users only once they bump.
- Each LTS line is maintained and released from its own branch (`0.2`, `1.4`), not from `main`: an LTS fix branches from and targets that branch. kili-python-sdk `release/*` and export `LTS-*` pin those versions.
- The optional dependencies (extras `coco`, `image`, `video`) are never imported bare: guard them (`try`/`except ImportError` at module level, or the import inside the function) and raise the `pip install kili-formats[<extra>]` hint when called without them. `kili_formats/__init__.py` imports every converter, so one bare import breaks `import kili_formats` on a plain install; CI's `build-test` catches it. Pillow is in `[dev]` only, as the reference the tests check imagesize against: `src` never imports it.
- pylint and pyright are not part of `pre-commit`: CI runs them, so a clean `pre-commit run --all-files` says nothing about them. CI's `pylint --rcfile=.pylintrc src/kili_formats` (must score 10.00/10) lints only the modules at the package root — `format/`, `media/` and `tool/` have no `__init__.py`, so it skips everything under them, `format/coco` and `format/geojson` included — while `pylint src` reaches them and reports findings on code nobody touched.
- The test matrix includes windows-latest, so anything that builds paths or writes files has to hold there too.
