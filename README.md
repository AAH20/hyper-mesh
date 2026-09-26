# ❖ Hyper-Mesh

> **Broker-Free P2P Kademlia Mesh Network for Distributed Frontier Agent Swarms**  
> Serverless peer discovery, logarithmic XOR metric routing, encrypted gossip propagation, and multi-attribute task auction consensus across edge nodes (**DeepSeek V4.1-Flash**) and cloud clusters (**GPT-6 Sol**, **Claude Opus 5.5**).

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![P2P](https://img.shields.io/badge/Network-Kademlia%20DHT%20Mesh-purple.svg)]()
[![Tests](https://img.shields.io/badge/Tests-3%2F3%20Passing-success.svg)]()

---

## ⚡ The Problem: The Fragile Central Message Broker

Today's multi-agent swarms rely on centralized cloud brokers (Redis, RabbitMQ, Kafka, central WebSockets):
1. **Single Point of Failure**: If the cloud coordinator restarts or experiences a network partition, all distributed agents collapse.
2. **Edge-to-Cloud Friction**: Coordinating agents across local developer laptops (Mac Studio), cloud H100 clusters, and edge devices requires complex ingress NAT configuration and firewall punching.
3. **Sub-Optimal Task Assignment**: Centralized brokers dispatch jobs without awareness of local model availability, latency, or compute pricing.

**Hyper-Mesh** provides a **Decentralized Sovereign Swarm Network**:
* **Kademlia DHT Peer Discovery**: Cryptographic node addressing and logarithmic XOR metric routing with zero central servers.
* **Resilient Gossip Broadcast**: Deduplicated gossip-sub protocol with hop-count boundaries that survives 50% node dropouts.
* **Multi-Attribute Task Auction**: Decentralized bidding balancing node reputation, model affinity, network latency, and execution cost.

---

## 📐 Architecture & P2P Mesh Topology

```mermaid
flowchart TD
    subgraph EdgeTier["Edge Nodes (Low Latency / Privacy)"]
        NodeEdge["Edge Node (Jetson / Orin)\nLocal: DeepSeek V4.1-Flash\nRole: EDGE_EXECUTOR"]
        NodeMac["Developer Laptop (Mac Studio)\nLocal: Claude Opus 5.5\nRole: COORDINATOR"]
    end

    subgraph CloudTier["Cloud Cluster (High-Throughput Reasoning)"]
        NodeCloud["Cloud Cluster (8x H100)\nLocal: GPT-6 Sol\nRole: CLOUD_ORACLE"]
        NodeStorage["Relay Node (Distributed NVMe)\nRole: STORAGE_RELAY"]
    end

    subgraph KademliaRouting["Decentralized Kademlia Overlay"]
        DHT["Kademlia 160-bit XOR Distance Routing Table\n(Logarithmic k-buckets)"]
        Gossip["Gossip-Sub Broadcast Engine\n(Deduplicated Message Relay)"]
        Auction["Multi-Attribute Task Auction Engine\n(Utility = 0.4*Rep + 0.3*Latency + 0.3*Cost)"]
    end

    NodeMac <-->|P2P Encrypted Tunnel| DHT
    NodeEdge <-->|P2P Encrypted Tunnel| DHT
    NodeCloud <-->|P2P Encrypted Tunnel| DHT
    NodeStorage <-->|P2P Encrypted Tunnel| DHT

    DHT --> Gossip
    Gossip --> Auction
    Auction -->|Task Assignment: Security Audit| NodeEdge
    Auction -->|Task Assignment: Formal Proof| NodeCloud
```

---

## 🚀 Key Modules
- **`hyper_mesh/dht_discovery.py`**: Implements 160-bit SHA-1 XOR distance metric and logarithmic k-bucket routing table.
- **`hyper_mesh/gossip_consensus.py`**: Deduplicated gossip propagation engine and multi-attribute task auction resolver.
- **`hyper_mesh/models.py`**: Data structures for `PeerNode`, `MeshMessage`, `TaskBidProposal`, and `NodeRole`.
- **`hyper_mesh/cli.py`**: Multi-node peer simulation and automated task auction demonstration.

---

## 🛠️ Installation & Usage

```bash
git clone https://github.com/AAH20/hyper-mesh.git
cd hyper-mesh
pip install -e .
```

### Run Demonstration
```bash
hyper-mesh --demo
```

### Run Unit Tests
```bash
python3 -m unittest discover tests
```
