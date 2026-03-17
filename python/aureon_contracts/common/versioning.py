from pydantic import BaseModel, ConfigDict, Field
import time
from typing import Optional

class BaseModelV1(BaseModel):
    """Base model for all V1 Canonical Contracts with strict validation."""
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True
    )

class CanonicalMeta(BaseModelV1):
    """Metadata for distributed messages to ensure versioning and compatibility."""
    version: str = Field(default="v1", description="Contract version (e.g., v1, v2)")
    schema_id: str = Field(..., description="Unique schema identifier for cross-language mapping")
    timestamp: int = Field(default_factory=lambda: int(time.time()), description="Unix timestamp for cross-language safety")
    trace_id: Optional[str] = Field(None, description="Correlation ID for distributed tracing (root trace)")
    request_id: Optional[str] = Field(None, description="Unique identifier for the specific request-response cycle")

from typing import Optional
