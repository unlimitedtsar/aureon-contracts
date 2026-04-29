# Integration Guide: Project Language -> Aureon Contracts

## Objective
Allow each project to express its own metadata language while preserving a single shared protocol.

## Decision Model
- Core protocol (shared by all): `schema/*.schema.json`
- Project extension (localized semantics): `schema/extensions/<namespace>/*`
- Runtime payloads carry extension data in namespaced metadata fields only.

## Steps To Add A Project Extension
1. Choose a stable namespace (example: `fraud_ops`, `research_lab`).
2. Copy template files from:
   - `schema/extensions/_template/extension_manifest.json`
   - `schema/extensions/_template/metadata.schema.json`
3. Create folder:
   - `schema/extensions/<namespace>/`
4. Update:
   - `extension_manifest.json` (`namespace`, owner, version, status)
   - `metadata.schema.json` (define optional extension fields)
5. Add sample payload under `examples/` if needed.
6. Run CI guards and open PR with integration notes.

## Payload Pattern
Chat/request side:
```json
{
  "meta_data": {
    "fraud_ops": {
      "risk_tier": "high",
      "rule_set": "v3"
    }
  }
}
```

Event side:
```json
{
  "meta": {
    "fraud_ops": {
      "signal": "suspicious_pattern",
      "confidence": 0.91
    }
  }
}
```

## Safety Rules
- Never remove or reinterpret core fields.
- Extension must be additive-only.
- Do not place extension keys at root payload level.
- Keep extension parser tolerant to unknown optional fields.

## Promotion To Core
If multiple projects use the same extension:
1. Open protocol evolution note.
2. Propose core schema addition (optional first).
3. Pass breaking-change guard and consistency checks.
4. Release with clear migration note.
