---
zenn_source: articles/datadog-log-pipeline-overview.md
substack_status: pending
substack_url: ""
---

# Inside Datadog's Log Pipeline: How "Logging without Limits" Actually Works

# Introduction

In this post, I want to walk through how Datadog processes logs internally — from raw ingestion all the way to indexed, queryable data.

If you've spent time clicking around Datadog's log management UI, you've probably noticed something satisfying: raw, messy log lines gradually get enriched and structured as they flow through the pipeline. It's a really elegant design, and once you understand the order in which things happen, it becomes clear why Datadog can offer both cost control and deep observability at the same time. Let me break it down.

:::message
This article focuses on the main steps I studied this time around. In practice, there are more detailed processes — sensitive data scanning, Error Tracking, Live Tail, and so on. For the full picture, please refer to the [official documentation | Datadog](https://docs.datadoghq.com/logs/).
:::

# The Overall Log Processing Flow

Datadog's log management is built around a design philosophy called **Logging without Limits™**, which lets you independently control "ingestion," "storage," and "analysis."

The high-level flow looks like this:

```
Ingest
  ↓
Pipelines (Parse & Enrich)
  ↓
Generate Metrics
  ↓
Exclusion Filters
  ↓
Index
```

# Walking Through Each Step

## Ingest

First, logs are collected into Datadog from a wide variety of sources.

Datadog offers **over 500 log integrations**, covering AWS, GCP, Kubernetes, and all kinds of middleware. I was honestly surprised by just how many there are.

## Pipelines (Parse & Enrich)

Once raw logs are ingested, they pass through **pipelines** that structure and enrich them (adding extra information).

Using processors like the **Grok parser**, unstructured text logs get broken down into fields, and additional attributes can be attached.

```
# Before parsing (raw log)
2024-04-27 12:00:00 ERROR [app] Connection timeout: host=db01 duration=5002ms

# After parsing (structured)
{
  "timestamp": "2024-04-27T12:00:00Z",
  "level": "ERROR",
  "service": "app",
  "message": "Connection timeout",
  "host": "db01",
  "duration_ms": 5002
}
```

Watching unformatted logs get cleaned up and enriched is honestly the most fun part of this whole process to observe.

## Generate Metrics

This is the most interesting part of the Logging without Limits design.

**Log-based metrics are generated *before* exclusion filters run.**

In other words, even for logs that will later be discarded and never make it to the index, you can still retain statistical information as metrics.

:::message
The benefit of this design is that even if you're aggressively dropping logs to keep costs down, you still get reliable metrics on trends, error rates, and the like.
:::

## Exclusion Filters

After metric generation, **exclusion filters** decide which logs are *not* saved to the index.

Debug logs, high-volume boilerplate logs, and anything that isn't needed for ongoing search can be dropped here, helping keep indexing costs under control.

## Index

Logs that pass through the filters are finally stored in the **Index**. Once a log is indexed, you can use Datadog's UI for facet search and analysis.

# Why This Ordering Matters

The key insight in this processing order is the design principle: **"extract metrics before throwing logs away."**

Log storage costs balloon quickly, so indexing every single log is rarely realistic. But if you just drop logs, you lose visibility into trends within the discarded data.

Logging without Limits solves this by placing metric generation *before* exclusion filters. You can lower storage costs while still maximizing observability.

# Wrap-up

Datadog's log pipeline has clearly separated stages: ingest, parse, generate metrics, exclude, and index. The design choice to run metric generation before exclusion filters strikes me as especially important — it's what allows you to balance cost and observability rather than trade one off against the other.

*Subscribe for more Datadog & Observability deep-dives.*
