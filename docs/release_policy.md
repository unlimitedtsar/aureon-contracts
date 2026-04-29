# Aureon Contracts Release Policy

## Goal
Keep contract evolution stable for all downstream systems that pin by git tag.

## Versioning Model
- Source of release truth: git tag.
- Python package version: derived from git tag via `setuptools-scm`.
- Local source fallback: `0.0.0+local` (non-release).

## Bump Rules
- Major (`X.0.0`):
  - Any breaking change in schema contract.
  - Removed field, type change, semantic incompatibility.
- Minor (`x.Y.0`):
  - Additive non-breaking fields/options.
  - New optional schema payloads.
- Patch (`x.y.Z`):
  - Documentation, CI, tooling, or non-contract bugfix.
  - No schema behavior change.

## Release Checklist
- `python aureon_contracts/ci/check_breaking_changes.py` passes.
- `python aureon_contracts/ci/check_schema_binding_consistency.py` passes.
- Python package build succeeds.
- Go compile check succeeds.
- Rust compile check succeeds.
- `README.md` and docs updated for user-facing changes.
- Tag note includes migration impact summary.

## Breaking Change Process
- Open architecture/protocol note before merge.
- Communicate migration path to consumer teams.
- Publish major tag only after migration guide is ready.
