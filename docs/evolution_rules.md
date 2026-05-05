---
type: source
tier: domain
domain: keystone
status: active
tags:
  - source
  - governance
---
# Aureon Protocol: Schema Evolution Laws

## Parent
[[START_HERE]]

## Depends On
[[SYSTEM_MANIFEST]]

## Related
[[ARCHITECTURE_LOCK]]


To maintain a stable, production-grade ecosystem and avoid "version hell," all developers must adhere to these absolute laws when modifying `aureon-contracts`.

## ⚖️ The Four Laws of Stability

1.  **Immutable Types**: NEVER change the data type of an existing field. (e.g., Changing an `int` to a `string` is a breaking change).
2.  **No Deletions**: NEVER remove a field from a model. If a field is deprecated, mark it as optional and document it, but do not delete it.
3.  **Additive-Only**: You may ONLY add new fields if they are **optional** (have a default value or are nullable).
4.  **Semantic Breaks**: Any change that violates the above rules MUST result in a major version bump (e.g., `v1` -> `v2`).

## 🔄 Versioning Policy

- **MAJOR (x.0.0)**: Breaking changes that require all ecosystem agents to upgrade (e.g., refactoring the Envelope).
- **MINOR (0.x.0)**: New features or models that are backward-compatible.
- **PATCH (0.0.x)**: Bug fixes or documentation updates that do not change the data shape.

## 🔒 Validation Strategy

- **Producer Responsibility**: Senders must validate payloads against the current schema before transmission.
- **Consumer Resilience**: Receivers should use strict validation (e.g., Pydantic's `extra="forbid"`) in development but consider "fail-soft" or logging for unknown fields in production to allow for staggered rollouts.
