import hashlib
from typing import Dict, List, Optional
from .models import PeerNode


def xor_distance(id1: str, id2: str) -> int:
    """Calculates the XOR distance metric between two SHA-1 node identifiers."""
    int1 = int(hashlib.sha1(id1.encode("utf-8")).hexdigest(), 16)
    int2 = int(hashlib.sha1(id2.encode("utf-8")).hexdigest(), 16)
    return int1 ^ int2


class KademliaRoutingTable:
    """
    Decentralized Kademlia routing table organizing peers into logarithmic buckets
    based on XOR metric distance.
    """

    def __init__(self, local_node_id: str, k_bucket_size: int = 8):
        self.local_node_id = local_node_id
        self.k_bucket_size = k_bucket_size
        self.peers: Dict[str, PeerNode] = {}

    def add_or_update_peer(self, peer: PeerNode):
        """Adds or updates a peer in the routing table."""
        if peer.node_id == self.local_node_id:
            return
        self.peers[peer.node_id] = peer

    def remove_peer(self, node_id: str):
        if node_id in self.peers:
            del self.peers[node_id]

    def find_closest_peers(self, target_id: str, count: int = 5) -> List[PeerNode]:
        """Returns the `count` closest peers to a given target ID using XOR distance."""
        sorted_peers = sorted(
            self.peers.values(),
            key=lambda p: xor_distance(p.node_id, target_id)
        )
        return sorted_peers[:count]

    def get_peers_by_model(self, model_name: str) -> List[PeerNode]:
        """Returns peers capable of running a specific frontier model."""
        return [p for p in self.peers.values() if model_name in p.supported_models]
