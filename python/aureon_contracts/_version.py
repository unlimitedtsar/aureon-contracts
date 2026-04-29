from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version


def resolve_version() -> str:
    # 1) Installed package metadata (preferred in released artifacts)
    try:
        return version("aureon-contracts")
    except PackageNotFoundError:
        pass

    # 2) CI/release injection from tag pipeline
    injected = os.getenv("AUREON_CONTRACTS_VERSION", "").strip()
    if injected:
        return injected

    # 3) Source checkout fallback
    return "0.0.0+local"


__version__ = resolve_version()
