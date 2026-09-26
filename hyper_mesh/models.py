from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
import time
import hashlib
import uuid


class NodeRole(str, Enum):
    COORDINATOR = "coordinator"
    EDGE_EXECUTOR = "edge_executor"
    CLOUD_ORACLE = "cloud_oracle"
    STORAGE_RELAY = "storage_relay"


@dataclass
class PeerNode:
    node_id: str
    ip_endpoint: str
    port: int
    role: NodeRole
    supported_models: List[str]  # e.g. ["DeepSeek V4.1-Flash", "GPT-6 Sol", "Claude Opus 5.5"]
    public_key: str
    last_seen: float = field(default_factory=time.time)
    reputation_score: float = 1.0


@dataclass
class MeshMessage:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    sender_id: str = ""
    recipient_id: Optional[str] = None  # None indicates broadcast / gossip
    topic: str = "swarm_gossip"
    payload: Dict[str, Any] = field(default_factory=dict)
    hop_count: int = 0
    max_hops: int = 5
    timestamp: float = field(default_factory=time.time)
    signature: str = ""


@dataclass
class TaskBidProposal:
    task_id: str
    bidder_node_id: str
    proposed_model: str
    estimated_latency_ms: float
    bid_price_credits: float
    reputation: float
    timestamp: float = field(default_factory=time.time)
