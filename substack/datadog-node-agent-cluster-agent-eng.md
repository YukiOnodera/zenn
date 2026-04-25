---
zenn_source: articles/datadog-node-agent-cluster-agent.md
published_zenn: false
substack_status: published
substack_url: "https://open.substack.com/pub/odryk/p/why-datadog-uses-two-agents-in-kubernetes"
---

# Why Datadog Uses Two Agents in Kubernetes: Node Agent vs Cluster Agent

If you've set up Datadog monitoring in a Kubernetes cluster, you've probably noticed there are *two* kinds of agents running: the **Node Agent** and the **Cluster Agent**. When I first encountered this, my reaction was: "Why do we need two? What's the difference?"

Once I understood the design intent, it all clicked. This post explains the two-tier architecture clearly — if you've had the same question, this is for you.

---

## The Overall Architecture

Datadog's Kubernetes monitoring is built on two components:

```
┌─────────────────────────────────────────┐
│               Kubernetes Cluster        │
│                                         │
│  ┌──────────┐  ┌──────────┐             │
│  │Node Agent│  │Node Agent│  ...        │  ← DaemonSet (one per node)
│  └────┬─────┘  └────┬─────┘             │
│       │              │                  │
│       └──────┬───────┘                  │
│              ↓                          │
│      ┌───────────────┐                  │
│      │ Cluster Agent │                  │  ← Deployment (one per cluster)
│      └───────┬───────┘                  │
│              ↓                          │
│       Kubernetes API Server             │
└─────────────────────────────────────────┘
```

Node Agents collect data from each individual node, while the Cluster Agent handles cluster-wide information centrally.

---

## What the Node Agent Does

The **Node Agent** runs as a `DaemonSet` — one instance per node in the cluster. Its scope is strictly limited to *that node*. It collects:

- Container metrics from pods running on that node
- Application logs and traces

After collecting data, it enriches it with cluster-wide metadata (Pod names, Service names, labels, etc.) received from the Cluster Agent, then ships everything to Datadog.

The key point: **Node Agents never talk directly to the Kubernetes API Server.** All cluster-wide information comes through the Cluster Agent.

---

## What the Cluster Agent Does

The **Cluster Agent** runs as a `Deployment` — typically just one instance per cluster. Unlike the Node Agent, it has a bird's-eye view of the entire cluster.

Its main responsibilities:

- **Proxying API Server access**: Fetches cluster-wide metadata (Pods, Services, Deployments, etc.) every 30 seconds and caches it
- **Distributing metadata to Node Agents**: Responds to Node Agent queries with cached metadata
- **Collecting Kubernetes events**: Gathers lifecycle events (Pod restarts, node status changes, etc.) and forwards them to Datadog

---

## Why Two Tiers? The Real Reason

This was the key insight for me.

**What if every Node Agent talked directly to the API Server?**

Imagine a cluster with 200 nodes. That's 200 Node Agents each periodically hitting the API Server with requests. At scale, this becomes a serious load problem — and could destabilize the cluster itself.

The Cluster Agent exists to solve exactly this:

```
Before (Node Agents hit API Server directly):
Node Agent × 200 → API Server  ← load explodes

After (via Cluster Agent):
Node Agent × 200 → Cluster Agent → API Server  ← single connection to API Server
                         ↑
                    distributes cached metadata
```

The Cluster Agent acts as a "representative" — it fetches and caches data from the API Server, then serves that cache to all Node Agents. This means **adding more nodes doesn't increase load on the API Server**.

There's a security benefit too: Node Agents no longer need direct API Server access, which means simpler, more minimal RBAC configurations.

---

## Wrapping Up

The "why are there two agents?" question answers itself once you think about scale. The two-tier design keeps API Server load flat as clusters grow, and simplifies permissions at the same time.

Understanding this architecture makes cluster monitoring diagrams much easier to read — and helps you debug issues when something goes wrong.

---

**References**

- [Cluster Agent for Kubernetes | Datadog Docs](https://docs.datadoghq.com/containers/cluster_agent/)
- [Set Up the Datadog Cluster Agent | Datadog Docs](https://docs.datadoghq.com/containers/cluster_agent/setup/)
- [Introducing the Datadog Cluster Agent | Datadog Blog](https://www.datadoghq.com/blog/datadog-cluster-agent/)

---

*If you found this useful, subscribe for more Datadog & Observability deep-dives. New posts every week.*
