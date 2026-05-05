---
type: source
tier: domain
domain: keystone
status: active
tags:
  - source
  - governance
---
# Consumer Migration Guide

## Parent
[[START_HERE]]

## Depends On
[[SYSTEM_MANIFEST]]

## Related
[[ARCHITECTURE_LOCK]]


## Scope
Guide for services that pin `aureon_contracts` by git tag.

## Upgrade Workflow
1. Read target tag release note and migration impact.
2. Update dependency pin to new tag.
3. Validate payloads against updated schemas.
4. Run integration tests for chat request/response and ARE telemetry paths.
5. Roll out progressively (staging -> canary -> production).

## Compatibility Expectations
- Minor tag upgrades should be additive and non-breaking.
- Major tag upgrades may require payload or parser updates.
- Patch tag upgrades should not change contract semantics.

## Common Migration Checks
- Envelope fields unchanged: `meta`, `identity`, `data`.
- Chat contracts: request/response still map correctly in provider adapters.
- ARE contracts: `ProviderHealthState`, `SystemEvent`, `PerformanceMetric` consumers still parse.
- Error contract: `code`, `message`, `retryable`, `provider_code` still consumed correctly.

## Rollback Plan
1. Revert dependency pin to previous tag.
2. Redeploy consumer service.
3. Record mismatch details and open contract issue with payload examples.

## Troubleshooting
- If parser fails on new field:
  - Ensure decoder allows unknown optional fields when appropriate.
- If contract guard fails in CI:
  - Review `ci/check_breaking_changes.py` output first.
  - For intentional break, execute major version process and migration comms.
