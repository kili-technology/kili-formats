<!--
    Review: 22/09/2026

    Rules for this file (Anthropic guidance):
    - keep it under 200 lines
    - `/doctor` trims anything Claude can derive from the code
    - every line must answer "would removing this make Claude get it wrong?"
    - no architecture summaries, no dependency lists, no file-by-file map (Claude reads those faster than we maintain them)
-->

# kili-formats

Label format conversions, published to PyPI as `kili-formats`.

## Gotchas

- **Publishing happens on a published GitHub Release, not on merge.** The version in `pyproject.toml` is bumped by hand and the release job refuses to run off a tag, so merging a format change ships nothing until someone cuts the release.
- Heavy dependencies live behind extras (`coco`, `image`, `video`). Importing numpy, shapely, Pillow or ffmpeg at the top level of the core package breaks a bare `pip install kili-formats` — CI catches it by installing without extras and importing one converter.
- pylint is **not** part of `pre-commit`: it runs in CI only, on `src/kili_formats`, and must score 10.00/10. A clean `pre-commit run --all-files` says nothing about it.
- The test matrix includes **windows-latest**, so anything that builds paths or writes files has to hold there too.
- `CONTRIBUTING.md` says Python 3.8, and `.pylintrc` (`py-version=3.8`) and pyupgrade (`--py38-plus`) agree with it — while `requires-python` is `>=3.10` and ruff targets py310. The lint configuration is the stale half.
