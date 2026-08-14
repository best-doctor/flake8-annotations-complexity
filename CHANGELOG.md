# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-14

### Added

- Support for Python 3.12, 3.13 and 3.14.
- `TAE003` (too long annotation) and its `--max-annotations-len` option are now documented.

### Changed

- **Breaking:** dropped support for Python 3.9. The minimum supported version is now 3.10.
- Packaging moved from `setup.py`/`setup.cfg` to a PEP 621 `pyproject.toml` built by hatchling.
- Development dependencies are managed with [uv](https://docs.astral.sh/uv/) and pinned in `uv.lock`.
- Linting moved from ~20 unmaintained flake8 plugins to [ruff](https://docs.astral.sh/ruff/);
  `safety` replaced with `pip-audit`; ruby `mdl` replaced with `markdownlint-cli2`.
- CI runs the test matrix on Python 3.10–3.14 and builds releases with `uv build`.

### Fixed

- Plugin crashed with `AttributeError` on Python 3.14, which removed `ast.Str`.
  String-wrapped annotations are now read via `ast.Constant`.
- Annotations of `async def` functions were never checked.
- Only regular arguments were checked. Positional-only, keyword-only, `*args`
  and `**kwargs` annotations were silently skipped.
- `--max-annotations-len` was ignored: `parse_options` never applied it, so `TAE003`
  always used the built-in default of 7.

### Removed

- Code Climate integration and its badges.

## [0.1.0] - 2025-02-27

### Changed

- **Breaking:** dropped support for Python older than 3.9.

### Fixed

- Incorrect complexity for `Literal` annotations containing string values.

[0.2.0]: https://github.com/best-doctor/flake8-annotations-complexity/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/best-doctor/flake8-annotations-complexity/compare/v0.0.8...v0.1.0
