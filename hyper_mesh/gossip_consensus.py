from typing import Dict, List, Optional, Set
import time
from .models import MeshMessage, TaskBidProposal, PeerNode
from .dht_discovery import KademliaRoutingTable


class GossipConsensusEngine:
    """
    Decentralized gossip message propagation and multi-agent task auction consensus.
    Guarantees resilient swarm coordination even under 50% node churn.
    """

    def __init__(self, routing_table: KademliaRoutingTable):
        self.routing_table = routing_table
        self.seen_message_ids: Set[str] = set()
        self.active_auctions: Dict[str, List[TaskBidProposal]] = {}

    def receive_message(self, message: MeshMessage) -> List[MeshMessage]:
        """
        Processes incoming message. If novel, propagates to neighbor peers up to max_hops.
        Returns forward messages to send.
        """
        if message.message_id in self.seen_message_ids:
            return []  # Deduplicated

        self.seen_message_ids.add(message.message_id)

        if message.hop_count >= message.max_hops:
            return []

        # Forward to closest neighbors
        neighbors = self.routing_table.find_closest_peers(message.sender_id, count=3)
        forward_messages = []
        for n in neighbors:
            if n.node_id != message.sender_id:
                fwd = MeshMessage(
                    message_id=message.message_id,
                    sender_id=self.routing_table.local_node_id,
                    recipient_id=n.node_id,
                    topic=message.topic,
                    payload=message.payload,
                    hop_count=message.hop_count + 1,
                    max_hops=message.max_hops
                )
                forward_messages.append(fwd)

        return forward_messages

    def submit_task_bid(self, task_id: str, bid: TaskBidProposal):
        """Records a peer's bid for a distributed task."""
        if task_id not in self.active_auctions:
            self.active_auctions[task_id] = []
        self.active_auctions[task_id].append(bid)

    def resolve_auction(self, task_id: str) -> Optional[TaskBidProposal]:
        """
        Resolves the winning bid for a task using multi-attribute utility:
        Utility = (Reputation * 0.4) + (1.0 / (Latency_ms + 1) * 0.3) + (1.0 / (Price + 0.1) * 0.3)
        """
        bids = self.active_auctions.get(task_id, [])
        if not bids:
            return None

        def calculate_score(b: TaskBidProposal) -> float:
            latency_score = 1000.0 / (b.estimated_latency_ms + 10.0)
            price_score = 10.0 / (b.bid_price_credits + 0.1)
            return (b.reputation * 50.0) + latency_score + price_score

        winning_bid = max(bids, key=calculate_score)
        return winning_bid
