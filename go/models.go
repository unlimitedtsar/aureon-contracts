package aureon_contracts

import (
	"encoding/json"
)

// CanonicalMeta represents metadata for distributed messages.
type CanonicalMeta struct {
	Version   string  `json:"version"`
	SchemaID  string  `json:"schema_id"`
	Timestamp int64   `json:"timestamp"`
	TraceID   *string `json:"trace_id,omitempty"`
	RequestID *string `json:"request_id,omitempty"`
}

// Identity represents distributed identity for tracking actors across boundaries.
type Identity struct {
	AgentID       string  `json:"agent_id"`
	TenantID      string  `json:"tenant_id"`
	SessionID     string  `json:"session_id"`
	CorrelationID *string `json:"correlation_id,omitempty"`
	OriginNode    *string `json:"origin_node,omitempty"`
}

// Envelope is a universal wrapper for distributed data exchange.
type Envelope struct {
	Meta     CanonicalMeta   `json:"meta"`
	Identity Identity        `json:"identity"`
	Data     json.RawMessage `json:"data"`
}

// ErrorResponse represents a standardized error contract.
type ErrorResponse struct {
	Code         string  `json:"code"`
	Message      string  `json:"message"`
	Retryable    bool    `json:"retryable"`
	ProviderCode *string `json:"provider_code,omitempty"`
}

// --- Keystone Chat Contracts ---

type CanonicalContentPart struct {
	Type     string  `json:"type"`
	Text     *string `json:"text,omitempty"`
	MimeType *string `json:"mime_type,omitempty"`
	Data     *string `json:"data,omitempty"`
}

type CanonicalChatMessage struct {
	Role       string                 `json:"role"`
	Content    []CanonicalContentPart `json:"content"`
	ToolCalls  []interface{}          `json:"tool_calls,omitempty"`
	ToolCallID *string                `json:"tool_call_id,omitempty"`
	Name       *string                `json:"name,omitempty"`
}

type CanonicalChatRequest struct {
	Model          string                 `json:"model"`
	Messages       []CanonicalChatMessage `json:"messages"`
	Tools          []interface{}          `json:"tools,omitempty"`
	ToolChoice     interface{}            `json:"tool_choice,omitempty"`
	Stream         bool                   `json:"stream"`
	Temperature    *float32               `json:"temperature,omitempty"`
	MaxTokens      *int                   `json:"max_tokens,omitempty"`
	TopP           *float32               `json:"top_p,omitempty"`
	Stop           interface{}            `json:"stop,omitempty"`
	SessionID      *string                `json:"session_id,omitempty"`
	ConversationID *string                `json:"conversation_id,omitempty"`
	MetaData       map[string]interface{} `json:"meta_data,omitempty"`
}

// --- ARE Monitoring Contracts ---

type PanicLevel string

const (
	PanicNone     PanicLevel = "NONE"
	PanicSoft     PanicLevel = "SOFT"
	PanicThrottle PanicLevel = "THROTTLE"
	PanicIsolate  PanicLevel = "ISOLATE"
	PanicRestore  PanicLevel = "RESTORE"
)

type ProviderHealthState struct {
	ProviderID string     `json:"provider_id"`
	PanicLevel PanicLevel `json:"panic_level"`
	HealthScore float32    `json:"health_score"`
	Version    int        `json:"version"`
	TS         int64      `json:"ts"`
	SenderID   string     `json:"sender_id"`
}

type SystemEvent struct {
	EventType string                 `json:"event_type"`
	TS        int64                  `json:"ts"`
	NodeID    string                 `json:"node_id"`
	Category  string                 `json:"category"`
	Meta      map[string]interface{} `json:"meta"`
	SenderID  string                 `json:"sender_id"`
}

type PerformanceMetric struct {
	ProviderID    string   `json:"provider_id"`
	FailureRate   float32  `json:"failure_rate"`
	LatencyP50    float32  `json:"latency_p50"`
	LatencyP95    *float32 `json:"latency_p95,omitempty"`
	StabilityScore float32  `json:"stability_score"`
	RequestCount  int      `json:"request_count"`
	ErrorCount    int      `json:"error_count"`
	TS            int64    `json:"ts"`
}
