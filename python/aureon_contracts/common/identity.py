from .versioning import BaseModelV1
from pydantic import Field
from typing import Optional

class Identity(BaseModelV1):
    """Distributed identity model for tracking agents, tenants, and sessions across layers."""
    agent_id: str = Field(..., description="Unique ID of the actor/agent")
    tenant_id: str = Field(..., description="Multi-tenant isolation identifier")
    session_id: str = Field(..., description="Logical session grouping")
    correlation_id: Optional[str] = Field(None, description="Physical request correlation ID")
    origin_node: Optional[str] = Field(None, description="The node ID where the message originated")
