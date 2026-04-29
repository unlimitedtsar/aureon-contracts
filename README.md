# Aureon Contracts

Canonical, versioned, zero-behavior contracts for the Keystone/Aureon ecosystem.

## Purpose
- Single protocol language across Python, Go, and Rust.
- Stable schema contracts for gateway, ARE telemetry, and distributed messaging.
- Strict evolution rules to prevent silent breaking changes.

## Quick Start
### Python
```bash
pip install aureon-contracts
```

```python
from aureon_contracts.keystone import CanonicalChatRequest

req = CanonicalChatRequest(
    model="gpt-4",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Hello"}]}],
)
```

### Go
```go
import contracts "github.com/unlimitedtsar/aureon-contracts/go"

req := contracts.CanonicalChatRequest{
    Model: "gpt-4",
    Stream: true,
}
```

## Repository Layout
```text
aureon_contracts/
  python/      # Python models (Pydantic v2)
  go/          # Go structs
  rust/        # Rust serde models
  schema/      # JSON Schema source of truth
  examples/    # Sample payloads
  ci/          # Breaking-change guard
  docs/        # Evolution and security notes
```

## Project-Specific Language Integration
You can extend metadata for specialized projects without changing core contracts.

Use extension lane:
```text
schema/extensions/<project_namespace>/
  extension_manifest.json
  metadata.schema.json
```

Integration rules:
- Keep core contracts in `schema/` unchanged.
- Add project-specific keys only under namespace metadata:
  - `meta_data.<project_namespace>.*` (chat/request side)
  - `meta.<project_namespace>.*` (event side)
- Extension fields must be optional and additive.
- Do not redefine meaning of core keys.
- If extension becomes cross-project, promote it to core through normal evolution process.

## Versioning (Important)
- Downstream projects pin this repo by git tag.
- Python package version is derived from git tags via `setuptools-scm`.
- Runtime `__version__` resolves from installed package metadata first.
- Fallback for local source checkout is `0.0.0+local`.

For CI/release pipelines, you can inject:
```bash
AUREON_CONTRACTS_VERSION=<tag>
```

## Contract Governance
- `schema/` is the protocol source of truth.
- `ci/check_breaking_changes.py` enforces compatibility against snapshots.
- Removing a schema that exists in snapshot is treated as breaking.
- Breaking changes require major version strategy and explicit migration plan.

## Evolution Rules
- No removal of published fields in the same major line.
- No type mutation of existing fields in the same major line.
- Additive changes only for minor versions.
- CI guard must pass before merge.

## Notes
- This repository contains data contracts only.
- No routing logic, model logic, or runtime state management belongs here.
