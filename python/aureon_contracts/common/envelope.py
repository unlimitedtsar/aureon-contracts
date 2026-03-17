from typing import Any, TypeVar, Generic
from .versioning import BaseModelV1, CanonicalMeta
from .identity import Identity
from pydantic import Field

T = TypeVar("T")

class Envelope(BaseModelV1, Generic[T]):
    """
    Standard Envelope wrapper for all distributed messages.
    Ensures that every data payload is accompanied by versioning, timing, and identity context.
    """
    meta: CanonicalMeta = Field(..., description="Versioning and timing metadata")
    identity: Identity = Field(..., description="Logical and physical identity of the sender")
    data: T = Field(..., description="The actual payload of the message")
