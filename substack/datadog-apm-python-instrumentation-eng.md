---
zenn_source: articles/datadog-apm-python-instrumentation.md
substack_status: pending
substack_url: ""
---

# Instrumenting Python Apps with Datadog APM: A Docker Setup Guide

# Introduction

In this post, we'll walk through the components required to instrument a Python application with Datadog APM, and how to configure them in a Docker environment.

A common shorthand is "just install the Datadog Agent and the tracing library and you're good to go" — and while that's essentially correct, understanding what each component is actually doing under the hood makes troubleshooting dramatically easier when things go wrong. If you've ever stared at an empty APM dashboard wondering why your traces aren't showing up, this guide should help you build a clearer mental model of how the pieces fit together.

# The Building Blocks of Datadog APM

To instrument an app with Datadog APM, you need to set up two things: the **Agent side** and the **library side**.

## Agent Side: The Trace Agent

When you enable APM in the Datadog Agent, an internal component called the **Trace Agent** starts up.

The Trace Agent is responsible for receiving trace data sent from your application and forwarding it to Datadog's backend. By default, it listens for traces on port **8126/tcp**.

In a Docker environment, you enable APM with the following environment variables:

| Environment Variable | Description |
| --- | --- |
| `DD_APM_ENABLED` | Enables APM (the Trace Agent) |
| `DD_APM_NON_LOCAL_TRAFFIC` | Allows trace submissions from other containers |

> If you don't set `DD_APM_NON_LOCAL_TRAFFIC=true`, traces from other containers on the same Docker network won't be accepted — watch out for this.

## Library Side: ddtrace

On the Python application side, you'll use a library called **ddtrace**. It's Datadog's official Python APM client and provides automatic instrumentation for over 80 libraries, including Flask, Django, and SQLAlchemy.

```sh
pip install ddtrace
```

# How Auto Instrumentation Works: Monkey Patching

ddtrace's auto instrumentation works through a technique called **Monkey Patching**.

**Monkey Patching** is a method of dynamically replacing existing classes or functions at runtime. ddtrace uses this approach to inject trace instrumentation into supported libraries without requiring any changes to your application code.

There are two ways to enable it.

## The ddtrace-run Command (Recommended)

Just prepend `ddtrace-run` to your application's startup command:

```sh
ddtrace-run python app.py
```

In a Dockerfile, modify the CMD like this:

```dockerfile:Dockerfile
CMD ["ddtrace-run", "python", "app.py"]
```

## import ddtrace.auto

Alternatively, you can import it at the very top of your entry point:

```python
import ddtrace.auto

from flask import Flask
# ...
```

> ⚠️ Using `ddtrace-run` and `import ddtrace.auto` at the same time will cause monkey patching to be applied twice, so use only one of them.

# Configuration in a Docker Environment

## Agent Container

```yaml:docker-compose.yml
services:
  datadog-agent:
    image: gcr.io/datadoghq/agent:latest
    environment:
      DD_API_KEY: ${DD_API_KEY}
      DD_SITE: datadoghq.com
      DD_APM_ENABLED: "true"
      DD_APM_NON_LOCAL_TRAFFIC: "true"
    ports:
      - "8126:8126/tcp"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## Application Container

On the application container side, specify the connection target for the Agent container via environment variables.

```yaml:docker-compose.yml
services:
  myapp:
    build: .
    environment:
      DD_AGENT_HOST: datadog-agent
      DD_TRACE_AGENT_PORT: "8126"
      DD_SERVICE: my-python-app
      DD_ENV: production
      DD_VERSION: 1.0.0
    depends_on:
      - datadog-agent
```

You can use the Docker Compose service name directly as the value of `DD_AGENT_HOST`.

# Unified Service Tagging

The three variables `DD_SERVICE` / `DD_ENV` / `DD_VERSION` are part of a mechanism called **Unified Service Tagging** — standard tags that link telemetry across all of Datadog.

| Environment Variable | Description | Example |
| --- | --- | --- |
| `DD_SERVICE` | Service name | `my-python-app` |
| `DD_ENV` | Environment name | `production`, `staging` |
| `DD_VERSION` | Version | `1.0.0` |

By setting these three, you'll be able to navigate from APM trace views to related logs and metrics with a single click. I strongly recommend configuring them.

# Conclusion

Datadog APM instrumentation works through the cooperation of two pieces: the Trace Agent on the Agent side, and ddtrace (with its monkey patching) on the library side. In a Docker environment, `DD_APM_NON_LOCAL_TRAFFIC=true` and `DD_AGENT_HOST` are particularly common gotchas, so keep them in mind during setup.

# References

[Tracing Docker Applications | Datadog](https://docs.datadoghq.com/containers/docker/apm/)

[Tracing Python Applications | Datadog](https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/dd_libraries/python/)

[Unified Service Tagging | Datadog](https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/)

*Subscribe for more Datadog & Observability deep-dives.*
