#!/usr/bin/env python3
"""Validate schema-to-binding consistency across Python/Go/Rust contracts."""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"
PYTHON_DIR = ROOT / "python" / "aureon_contracts"
GO_FILE = ROOT / "go" / "models.go"
RUST_FILE = ROOT / "rust" / "src" / "lib.rs"
EXTENSIONS_DIR = SCHEMA_DIR / "extensions"


REQUIRED_SCHEMA_FILES = {
    "envelope.schema.json",
    "common_meta.schema.json",
    "identity.schema.json",
    "error_response.schema.json",
    "keystone_chat_request.schema.json",
    "keystone_chat_response.schema.json",
    "provider_health_state.schema.json",
    "system_event.schema.json",
    "performance_metric.schema.json",
    "are_metric.schema.json",
    "are_neuro_state.schema.json",
    "are_event.schema.json",
}

PYTHON_SYMBOLS = {
    "common/envelope.py": ["class Envelope"],
    "common/versioning.py": ["class CanonicalMeta"],
    "common/identity.py": ["class Identity"],
    "common/errors.py": ["class ErrorResponse"],
    "keystone/models.py": ["class CanonicalChatRequest", "class CanonicalChatResponse"],
    "are/models.py": ["class ProviderHealthState"],
    "are/events.py": ["class SystemEvent"],
    "are/metrics.py": ["class PerformanceMetric"],
}

GO_SYMBOLS = [
    "type Envelope struct",
    "type CanonicalMeta struct",
    "type Identity struct",
    "type ErrorResponse struct",
    "type CanonicalChatRequest struct",
    "type ProviderHealthState struct",
    "type SystemEvent struct",
    "type PerformanceMetric struct",
]

RUST_SYMBOLS = [
    "pub struct Envelope",
    "pub struct CanonicalMeta",
    "pub struct Identity",
    "pub struct ErrorResponse",
    "pub struct CanonicalChatRequest",
    "pub struct ProviderHealthState",
    "pub struct SystemEvent",
    "pub struct PerformanceMetric",
]


def fail(msg: str) -> None:
    print(f"[CONSISTENCY][FAIL] {msg}")
    sys.exit(1)


def main() -> None:
    missing_schema = sorted(f for f in REQUIRED_SCHEMA_FILES if not (SCHEMA_DIR / f).exists())
    if missing_schema:
        fail(f"Missing required schema files: {missing_schema}")

    for rel_path, tokens in PYTHON_SYMBOLS.items():
        p = PYTHON_DIR / rel_path
        if not p.exists():
            fail(f"Missing Python binding file: {rel_path}")
        text = p.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                fail(f"Missing Python symbol '{token}' in {rel_path}")

    go_text = GO_FILE.read_text(encoding="utf-8")
    for token in GO_SYMBOLS:
        if token not in go_text:
            fail(f"Missing Go symbol '{token}' in go/models.go")

    rust_text = RUST_FILE.read_text(encoding="utf-8")
    for token in RUST_SYMBOLS:
        if token not in rust_text:
            fail(f"Missing Rust symbol '{token}' in rust/src/lib.rs")

    # Simple guard: schema filename prefix should have at least one likely contract symbol in any binding.
    all_binding_text = "\n".join(
        [
            go_text.lower(),
            rust_text.lower(),
            *( (PYTHON_DIR / rel).read_text(encoding="utf-8").lower() for rel in PYTHON_SYMBOLS.keys() ),
        ]
    )
    suspicious = []
    for schema in REQUIRED_SCHEMA_FILES:
        stem = schema.replace(".schema.json", "")
        hints = re.split(r"[_\-]", stem)
        if not any(h in all_binding_text for h in hints if len(h) > 3):
            suspicious.append(schema)
    if suspicious:
        fail(f"Schema files have no binding hints (possible orphan contracts): {sorted(suspicious)}")

    # Extension lane checks (no core binding requirement, but must be structurally valid).
    if EXTENSIONS_DIR.exists():
        for namespace_dir in EXTENSIONS_DIR.iterdir():
            if not namespace_dir.is_dir():
                continue
            if namespace_dir.name.startswith("_"):
                continue

            manifest = namespace_dir / "extension_manifest.json"
            if not manifest.exists():
                fail(f"Missing extension manifest: {manifest.relative_to(ROOT)}")

            try:
                manifest_obj = json.loads(manifest.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                fail(f"Invalid JSON in {manifest.relative_to(ROOT)}: {exc}")

            ns = manifest_obj.get("namespace")
            if ns != namespace_dir.name:
                fail(
                    f"Extension namespace mismatch in {manifest.relative_to(ROOT)}: "
                    f"namespace='{ns}' folder='{namespace_dir.name}'"
                )

            files = manifest_obj.get("files", [])
            if not isinstance(files, list) or not files:
                fail(f"Extension manifest must define non-empty 'files': {manifest.relative_to(ROOT)}")

            for rel in files:
                p = namespace_dir / rel
                if not p.exists():
                    fail(f"Extension manifest references missing file: {p.relative_to(ROOT)}")
                try:
                    json.loads(p.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    fail(f"Invalid JSON in extension file {p.relative_to(ROOT)}: {exc}")

    print("[CONSISTENCY][PASS] Schema and bindings are consistent at required surface.")


if __name__ == "__main__":
    main()
