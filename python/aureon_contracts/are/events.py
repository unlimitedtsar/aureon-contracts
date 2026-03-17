from enum import Enum
import time
from typing import Optional, Dict, Any
from pydantic import Field
from ..common.versioning import BaseModelV1

class EventType(str, Enum):
    """Standardized event types for global momentum parity and tracking."""
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    TIMEOUT = "timeout"
    PANIC = "panic"
    SECURITY_ALERT = "security_alert"
    SYSTEM_MOMENTUM = "system_momentum"

class SystemEvent(BaseModelV1):
    """
    Standardized event model for distributed system coordination.
    Aligns with the Protocol Layer specification (type, timestamp, source, payload).
    """
    event_type: EventType = Field(..., description="The hierarchical type of the event (e.g., PANIC, ERROR)")
    ts: int = Field(default_factory=lambda: int(time.time()), description="Unix timestamp of when the event occurred")
    node_id: str = Field(..., description="The source node or agent that generated the event")
    category: str = Field(..., description="High-level category (e.g., security, infrastructure)")
    meta: Dict[str, Any] = Field(default_factory=dict, description="The event payload (opaque dictionary)")
    sender_id: str = Field(..., description="The physical sender ID (for relay tracking)")
