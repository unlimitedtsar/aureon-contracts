from enum import Enum
from typing import Optional, Dict, Any
from ..common.versioning import BaseModelV1

class PanicLevel(str, Enum):
    NONE = "NONE"
    SOFT = "SOFT"
    THROTTLE = "THROTTLE"
    ISOLATE = "ISOLATE"
    RESTORE = "RESTORE"

class InfraState(str, Enum):
    FULL = "FULL"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"

class ComponentStatus(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    RECONNECTING = "RECONNECTING"

class ProviderHealthState(BaseModelV1):
    """Authoritative representation of a provider's health state for distributed coordination."""
    provider_id: str
    panic_level: PanicLevel
    health_score: float
    version: int
    ts: int  # Unix timestamp for cross-language compatibility
    sender_id: str
