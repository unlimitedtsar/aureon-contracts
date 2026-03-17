from ..common.versioning import BaseModelV1
from pydantic import Field

class ErrorResponse(BaseModelV1):
    """Standardized error contract for the entire Aureon ecosystem."""
    code: str = Field(..., description="Machine-readable error code (e.g., PROVIDER_TIMEOUT)")
    message: str = Field(..., description="Human-readable error description")
    retryable: bool = Field(default=False, description="Whether the request can be safely retried")
    provider_code: str | None = Field(None, description="Original error code from the underlying provider")
