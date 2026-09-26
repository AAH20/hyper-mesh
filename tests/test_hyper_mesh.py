import unittest
from hyper_mesh.models import PeerNode, NodeRole, TaskBidProposal, MeshMessage
from hyper_mesh.dht_discovery import KademliaRoutingTable, xor_distance
from hyper_mesh.gossip_consensus import GossipConsensusEngine


class TestHyperMesh(unittest.TestCase):
    def setUp(self):
        self.table = KademliaRoutingTable(local_node_id="local-node")
        self.consensus = GossipConsensusEngine(routing_table=self.table)

    def test_xor_distance_metric(self):
        dist_self = xor_distance("node-a", "node-a")
        self.assertEqual(dist_self, 0)

        dist_diff = xor_distance("node-a", "node-b")
        self.assertGreater(dist_diff, 0)
        # Symmetry
        self.assertEqual(dist_diff, xor_distance("node-b", "node-a"))

    def test_routing_table_and_model_filtering(self):
        p1 = PeerNode("node-1", "10.0.0.1", 8000, NodeRole.CLOUD_ORACLE, ["Claude Opus 5.5"], "pk1")
        p2 = PeerNode("node-2", "10.0.0.2", 8000, NodeRole.EDGE_EXECUTOR, ["DeepSeek V4.1-Flash"], "pk2")
        self.table.add_or_update_peer(p1)
        self.table.add_or_update_peer(p2)

        self.assertEqual(len(self.table.peers), 2)
        closest = self.table.find_closest_peers("target-hash", count=1)
        self.assertEqual(len(closest), 1)

        opus_peers = self.table.get_peers_by_model("Claude Opus 5.5")
        self.assertEqual(len(opus_peers), 1)
        self.assertEqual(opus_peers[0].node_id, "node-1")

    def test_gossip_deduplication_and_auction(self):
        p1 = PeerNode("node-1", "10.0.0.1", 8000, NodeRole.CLOUD_ORACLE, ["Claude Opus 5.5"], "pk1")
        self.table.add_or_update_peer(p1)

        msg = MeshMessage(
            message_id="msg-unique-123",
            sender_id="node-1",
            payload={"task": "ping"}
        )
        fwd1 = self.consensus.receive_message(msg)
        self.assertIn("msg-unique-123", self.consensus.seen_message_ids)

        # Duplicate receive should return empty
        fwd2 = self.consensus.receive_message(msg)
        self.assertEqual(len(fwd2), 0)

        # Auction test
        b1 = TaskBidProposal("t1", "p1", "Claude Opus 5.5", 500.0, 5.0, 0.9)
        b2 = TaskBidProposal("t1", "p2", "DeepSeek V4.1-Flash", 50.0, 0.5, 0.95)
        self.consensus.submit_task_bid("t1", b1)
        self.consensus.submit_task_bid("t1", b2)

        winner = self.consensus.resolve_auction("t1")
        self.assertIsNotNone(winner)
        self.assertEqual(winner.bidder_node_id, "p2")


if __name__ == "__main__":
    unittest.main()
