use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Metadata for distributed messages ensuring versioning and timing consistency.
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct CanonicalMeta {
    pub version: String,
    pub schema_id: String,
    pub timestamp: i64,
    pub trace_id: Option<String>,
    pub request_id: Option<String>,
}

/// Distributed identity for tracking actors across service boundaries.
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct Identity {
    pub agent_id: String,
    pub tenant_id: String,
    pub session_id: String,
    pub correlation_id: Option<String>,
    pub origin_node: Option<String>,
}

/// Universal wrapper for distributed data exchange.
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct Envelope<T> {
    pub meta: CanonicalMeta,
    pub identity: Identity,
    pub data: T,
}

/// Standardized error contract for the entire Aureon ecosystem.
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct ErrorResponse {
    pub code: String,
    pub message: String,
    pub retryable: bool,
    pub provider_code: Option<String>,
}

// --- Keystone Chat Contracts ---

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct CanonicalContentPart {
    #[serde(rename = "type")]
    pub part_type: String,
    pub text: Option<String>,
    pub mime_type: Option<String>,
    pub data: Option<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct CanonicalChatMessage {
    pub role: String,
    pub content: Vec<CanonicalContentPart>,
    pub tool_calls: Option<Vec<HashMap<String, serde_json::Value>>>,
    pub tool_call_id: Option<String>,
    pub name: Option<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct CanonicalChatRequest {
    pub model: String,
    pub messages: Vec<CanonicalChatMessage>,
    pub tools: Option<Vec<serde_json::Value>>,
    pub tool_choice: Option<serde_json::Value>,
    pub stream: bool,
    pub temperature: Option<f32>,
    pub max_tokens: Option<i32>,
    pub top_p: Option<f32>,
    pub stop: Option<serde_json::Value>,
    pub session_id: Option<String>,
    pub conversation_id: Option<String>,
    pub meta_data: Option<HashMap<String, serde_json::Value>>,
}

// --- ARE Monitoring Contracts ---

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "UPPERCASE")]
pub enum PanicLevel {
    None,
    Soft,
    Throttle,
    Isolate,
    Restore,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct ProviderHealthState {
    pub provider_id: String,
    pub panic_level: PanicLevel,
    pub health_score: f32,
    pub version: i32,
    pub ts: i64,
    pub sender_id: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct SystemEvent {
    pub event_type: String,
    pub ts: i64,
    pub node_id: String,
    pub category: String,
    pub meta: HashMap<String, serde_json::Value>,
    pub sender_id: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub struct PerformanceMetric {
    pub provider_id: String,
    pub failure_rate: f32,
    pub latency_p50: f32,
    pub latency_p95: Option<f32>,
    pub stability_score: f32,
    pub request_count: i32,
    pub error_count: i32,
    pub ts: i64,
}
