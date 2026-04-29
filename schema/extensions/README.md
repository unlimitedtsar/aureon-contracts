# Extension Schemas

This directory is for project-specific, non-core contract extensions.

Rules:
- Do not modify or override core schema semantics in `../`.
- Extensions must be additive and optional.
- Use namespaced keys under payload metadata:
  - `meta_data.<project_namespace>.*` for chat/request metadata
  - `meta.<project_namespace>.*` for event metadata
- One project = one namespace folder.

Recommended layout:
```text
schema/extensions/
  <project_namespace>/
    extension_manifest.json
    metadata.schema.json
```
