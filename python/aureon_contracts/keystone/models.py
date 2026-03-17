from typing import List, Dict, Any, Optional, Union
from pydantic import Field
from ..common.versioning import BaseModelV1

class CanonicalContentPart(BaseModelV1):
    """A single part of a message's content (e.g., text or image)."""
    type: str = Field("text", pattern="^(text|image)$")
    text: Optional[str] = None
    mime_type: Optional[str] = None
    data: Optional[str] = None # base64 encoded data

class CanonicalChatMessage(BaseModelV1):
    """A single message in a conversation, in a neutral format."""
    role: str = Field(..., pattern="^(system|user|assistant|tool)$")
    content: List[CanonicalContentPart] = Field(default_factory=list)
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None

class CanonicalTool(BaseModelV1):
    """A tool definition, in a neutral format."""
    type: str = "function"
    function: Dict[str, Any]

class CanonicalChatRequest(BaseModelV1):
    """The internal, provider-agnostic representation of a chat completion request."""
    model: str
    messages: List[CanonicalChatMessage]
    tools: Optional[List[CanonicalTool]] = None
    tool_choice: Optional[Union[str, Dict]] = None
    stream: bool = False
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    stop: Optional[Union[str, List[str]]] = None
    
    # Metadata for routing & tracking
    has_vision_input: bool = False
    requested_json_mode: bool = False
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_legacy(cls, data: Dict[str, Any]) -> "CanonicalChatRequest":
        """Map legacy dictionary data to current canonical model."""
        # Implementation for backward compatibility
        return cls(**data)

class CanonicalChoice(BaseModelV1):
    """A single choice in a canonical response."""
    index: int
    message: CanonicalChatMessage
    finish_reason: Optional[str] = None

class CanonicalUsage(BaseModelV1):
    """Token usage details in a canonical format."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    provider_id: Optional[str] = None

class CanonicalChatResponse(BaseModelV1):
    """The internal, provider-agnostic representation of a chat completion response."""
    id: str
    model: str
    choices: List[CanonicalChoice]
    usage: Optional[CanonicalUsage] = None
    latency_ms: Optional[int] = None
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None
