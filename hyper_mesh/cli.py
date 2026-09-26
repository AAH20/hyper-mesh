import argparse
from .models import PeerNode, NodeRole, TaskBidProposal, MeshMessage
from .dht_discovery import KademliaRoutingTable
from .gossip_consensus import GossipConsensusEngine


def main():
    parser = argparse.ArgumentParser(description="hyper-mesh: Broker-Free P2P Kademlia Mesh Network for Distributed Swarms")
    parser.add_argument("--demo", action="store_true", help="Run simulated P2P mesh cluster")
    args = parser.parse_args()

    print("=== hyper-mesh v1.0.0 (Frontier September 2026) ===")
    print("[*] Initializing Local P2P Node (node-mac-studio)...")

    local_table = KademliaRoutingTable(local_node_id="node-mac-studio")
    consensus = GossipConsensusEngine(routing_table=local_table)

    # Register distributed peer nodes
    p1 = PeerNode(
        node_id="node-h100-cloud",
        ip_endpoint="192.168.10.45",
        port=9001,
        role=NodeRole.CLOUD_ORACLE,
        supported_models=["GPT-6 Sol", "Claude Opus 5.5"],
        public_key="ed25519:pubkey_cloud_01",
        reputation_score=0.98
    )
    p2 = PeerNode(
        node_id="node-edge-orin",
        ip_endpoint="192.168.10.78",
        port=9002,
        role=NodeRole.EDGE_EXECUTOR,
        supported_models=["DeepSeek V4.1-Flash", "Gemini 3.8 Flash Cyber"],
        public_key="ed25519:pubkey_edge_02",
        reputation_score=0.92
    )

    local_table.add_or_update_peer(p1)
    local_table.add_or_update_peer(p2)

    print(f"[*] Registered {len(local_table.peers)} peers in Kademlia routing table.")

    # Auction demo
    task_id = "task-sec-audit-902"
    print(f"\n[*] Broadcasting task auction for: '{task_id}' (Requires Fast Cyber Analysis)...")

    consensus.submit_task_bid(
        task_id=task_id,
        bid=TaskBidProposal(
            task_id=task_id,
            bidder_node_id=p1.node_id,
            proposed_model="Claude Opus 5.5",
            estimated_latency_ms=450.0,
            bid_price_credits=2.5,
            reputation=p1.reputation_score
        )
    )
    consensus.submit_task_bid(
        task_id=task_id,
        bid=TaskBidProposal(
            task_id=task_id,
            bidder_node_id=p2.node_id,
            proposed_model="DeepSeek V4.1-Flash",
            estimated_latency_ms=45.0,
            bid_price_credits=0.2,
            reputation=p2.reputation_score
        )
    )

    winner = consensus.resolve_auction(task_id)
    if winner:
        print(f"    - Winning Bidder: {winner.bidder_node_id}")
        print(f"    - Model Selected: {winner.proposed_model}")
        print(f"    - Est. Latency:   {winner.estimated_latency_ms} ms")
        print(f"    - Cost:           {winner.bid_price_credits} credits")

    print("\n[*] hyper-mesh P2P gossip cluster operating with zero central brokers.")


if __name__ == "__main__":
    main()
