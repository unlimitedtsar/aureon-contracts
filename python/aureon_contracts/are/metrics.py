from typing import Optional
from ..common.versioning import BaseModelV1
from pydantic import Field

class PerformanceMetric(BaseModelV1):
    """Unified metric model for agent performance and stability tracking."""
    provider_id: str
    failure_rate: float = Field(0.0, ge=0.0, le=1.0)
    latency_p50: float = Field(..., description="P50 latency in milliseconds")
    latency_p95: Optional[float] = Field(None, description="P95 latency in milliseconds")
    stability_score: float = Field(..., ge=0.0, le=1.0)
    request_count: int = Field(0, ge=0)
    error_count: int = Field(0, ge=0)
    ts: int  # Unix timestamp
