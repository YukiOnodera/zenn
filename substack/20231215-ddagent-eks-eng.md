---
zenn_source: articles/20231215-ddagent-eks.md
published_zenn: true
substack_status: draft
substack_url: ""
---

# Why Setting Up Datadog on EKS Is Trickier Than You'd Expect

# Introduction

Deploying Datadog on Amazon EKS sounds straightforward at first — after all, Datadog has solid Kubernetes support and AWS is one of its most popular integrations. In practice, however, I ran into more friction than I expected when getting Datadog up and running on EKS, especially once Fargate entered the picture. The official documentation is comprehensive, but it's scattered across multiple pages, and there isn't a single place that lays out the full picture for EKS users.

This post organizes what I learned, with a focus on the gotchas that cost me time. If you're planning a Datadog rollout on EKS — particularly with mixed EC2 and Fargate workloads — hopefully this saves you some headaches.

# Overview

When deploying Datadog on EKS, you need to install the Datadog Agent differently depending on whether you're running EKS on EC2 or EKS on Fargate.

If you're running a mixed workload that uses both EC2 and Fargate, you'll need to install an Agent suited to each workload type.

## Datadog Agent on EKS with EC2

In this configuration, just like with regular EC2, you need one Agent per node.

For EKS specifically, you basically follow the instructions in the [Kubernetes](https://docs.datadoghq.com/ja/containers/kubernetes/) documentation.

> The recommended installation method is to use the Operator.

## Datadog Agent on EKS with Fargate

This configuration is similar to ECS tasks — you need to deploy the Agent as a sidecar to each Pod.

Datadog provides official documentation at [Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB), so it's best to follow that guide.

In addition, if you're running a mixed workload and want to use the Datadog Cluster Agent, extra configuration is required. The setup is also described in the [Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#cluster-agent-%E3%81%BE%E3%81%9F%E3%81%AF-cluster-checks-runner-%E3%81%AE%E5%AE%9F%E8%A1%8C) docs.

# Things to Watch Out For

1. **When using the Datadog Cluster Agent, make sure it's deployed on an EC2 node — not on Fargate.** I missed this and spent a fair amount of time troubleshooting before realizing the issue.
2. **Environment variable settings, including tags, must be configured separately for each Agent.** If you're managing things via IaC this can feel redundant, but it's unavoidable.
3. **If you're using Fargate, costs scale with the number of Pods.** Estimate your costs in advance before scaling up.

# Conclusion

Deploying the Datadog Agent on EKS gets surprisingly complex once you account for different workload types.

I couldn't find a single place in the official documentation that covered the full picture in a structured way, so it was useful to organize my own notes here.

# References

[Kubernetes](https://docs.datadoghq.com/ja/containers/kubernetes/)

[Amazon EKS on AWS Fargate](https://docs.datadoghq.com/ja/integrations/eks_fargate/#%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)

*Subscribe for more Datadog & Observability deep-dives.*
