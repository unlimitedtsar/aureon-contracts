# Aureon Contracts

[![Protocol Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](docs/evolution_rules.md)
[![Language Support](https://img.shields.io/badge/languages-Python%20|%20Go%20|%20Rust-green.svg)](#usage)
[![Security Audit](https://img.shields.io/badge/security-Self--Audited%20(v1)-brightgreen.svg)](docs/security_audit_v1.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Aureon Contracts** is the source of truth for all canonical data structures and distributed protocols within the Keystone and Aureon AI ecosystem. It provides a provider-agnostic, versioned interface for inter-agent communication, telemetry, and health coordination.

## ⚡ Quick Start

### 1. Python
```bash
pip install aureon-contracts
```

```python
from aureon_contracts.common import Envelope
from aureon_contracts.keystone import CanonicalChatRequest

# Initialize a canonical request
req = CanonicalChatRequest(model="gpt-4", messages=[{"role": "user", "content": [{"type": "text", "text": "Hello!"}]}])
```

### 2. Go
```go
import contracts "github.com/unlimitedtsar/aureon-contracts/go"

// native struct usage
req := contracts.CanonicalChatRequest{
    Model: "gpt-4",
    Stream: true,
}
```

---

## 🏗 Repository Structure

This is a polyglot repository designed to be a "Zero-Behavior" protocol layer:

```text
aureon_contracts/
  ├── python/      # Python 3.10+ implementation (Pydantic v2)
  ├── go/          # Go 1.21+ implementation (Naked structs)
  ├── rust/        # Rust implementation (Serde-ready)
  ├── schema/      # JSON Schemas (The universal source of truth)
  ├── examples/    # Sample payloads for Chat, Health, and Events
  ├── ci/          # Protocol Guard (Breaking change detection)
  └── docs/        # Evolution rules and security audit reports
```

## � Design Principles

- **Zero Behavior**: No business logic in contracts. Only data shapes.
- **Deterministic**: Fully predictable schema behavior across all languages.
- **Cross-Language First**: Designed for multi-runtime systems (Python, Go, Rust).
- **Backward Compatible**: No breaking changes in minor versions (Strict Evolution laws).

## 👥 Who is this for?

- **AI Gateway developers** building LLM proxies.
- **Multi-agent system builders** requiring reliable coordination.
- **LLM infrastructure engineers** standardizing observability.
- **External plugin / tool developers** integrating with the Aureon ecosystem.

## 🚫 Non-Goals

- This repository does **NOT** implement routing or load-balancing logic.
- This repository does **NOT** include AI models or weights.
- This repository does **NOT** manage application state or databases.

---

## �🧠 Core Concepts

### 1. The Canonical Model
All external schemas (OpenAI, Gemini, Claude, etc.) are translated into a **Canonical Model** at the gateway. This ensures that downstream agents and services only ever interact with a stable, internal interface.

### 2. The Envelope Pattern
Every message exchange follows the **Envelope** pattern, wrapping physical data with distributed context:

```json
{
  "meta": {
    "version": "v1.0.0",
    "schema_id": "common_meta",
    "timestamp": 1710680000,
    "request_id": "req_123",
    "trace_id": "trace_abc"
  },
  "identity": {
    "agent_id": "agent_primary",
    "tenant_id": "tenant_default",
    "session_id": "session_999"
  },
  "data": {
    "model": "gpt-4",
    "messages": [
      {
        "role": "user",
        "content": [{"type": "text", "text": "What is the status of the system?"}]
      }
    ]
  }
}
```

---

## ❗ Error Handling

All errors in the ecosystem follow a standardized contract to enable reliable decision-making in the ARE (Aureon Runtime Engine):

```json
{
  "code": "PROVIDER_TIMEOUT",
  "message": "The upstream provider failed to respond within 30s",
  "retryable": true,
  "provider_code": "504"
}
```

---

## 🔄 Version Compatibility

| Version | Status | Notes |
|---------|--------|-------|
| v1.x    | Stable | Production ready. Active development. |
| v0.x    | Deprecated | Experimental. Do not use in production. |

---

## ⚖️ Evolution Rules (Protocol Laws)

To maintain ecosystem stability, this repository enforces strict **Evolution Laws**:
- **Immutability**: Once a field is published in a major version, it can never be removed or its type changed.
- **Additivity**: Only new optional fields may be added to existing models.
- **Safety Guard**: Every PR is automatically scanned by the [Breaking Change Guard](ci/check_breaking_changes.py). Any violation will fail the CI.

Consult [docs/evolution_rules.md](docs/evolution_rules.md) for full details.

---

## 🛡 Security
This module focuses on **Zero-Secret Hygiene**. It contains no logic, only data shapes. For internal audit findings and sanitization recommendations, see [docs/security_audit_v1.md](docs/security_audit_v1.md).

## 📄 License
Released under the [MIT License](LICENSE).
