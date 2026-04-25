---
zenn_source: articles/datadog-asm-protection.md
published_zenn: true
substack_status: draft
substack_url: ""
---

# Datadog ASM Protection: The Best Bang-for-Your-Buck Application Security I've Used

# Introduction

In this post, I want to walk through the **Protection** features that come with Datadog ASM (Application Security Management).

If you're already using Datadog for APM and observability, ASM is a natural extension that brings application-layer security into the same pane of glass — letting you detect, investigate, and block threats without standing up a separate security stack. For teams that want strong protection without the operational overhead of a dedicated WAF platform, it's surprisingly capable.

https://docs.datadoghq.com/security/application_security/threats/protection/

Datadog ASM offers several capabilities beyond Protection — such as Traces and Signals — that work hand-in-hand with it, but in this article I'll focus specifically on Protection.

For a broader overview of Datadog ASM, check this out:

https://zenn.dev/yukionodera/articles/datadog-securities-services

# What is Datadog ASM's Protection Feature?

Datadog Application Security Monitoring (ASM) provides blocking capabilities for requests and users that are identified as threats. **Protection** is the umbrella term for these blocking features.

Below, I've organized and summarized the most noteworthy aspects of Protection.

## Deny List and Pass List

Datadog ASM lets you create **Deny Lists and Pass Lists** based on IP addresses or paths.

First, a **Deny List** lets you block requests based on IP address or User ID.

You can also apply temporary access restrictions — for example, 15 minutes — which is useful for protecting against specific threats.

This is mainly used in conjunction with Detection Rules and Signals.

Next, a **Pass List** lets you specify traffic that you don't want to block, by IP, path, and so on.

You can also configure things like "don't block this specific rule" or "monitor requests but don't block them."

## IP Block

Datadog ASM provides a feature for **easily blocking IP addresses directly from the GUI console**. This integrates seamlessly with the Deny List mentioned above, so you can review the list of blocked IP addresses afterward.

You can also block addresses with a **time limit such as 15 minutes**, which I've personally found extremely handy.

The ability to leave a memo when blocking an IP is a **subtly useful feature** as well.

## In-App WAF

Datadog ASM's **In-App WAF** is a powerful security feature that identifies and blocks **suspicious requests** at the application level.

Inspection of suspicious requests is performed by the Datadog libraries, and recognized requests appear in the Trace Explorer (Traces).

The request information in the Trace Explorer can also be used as a basis for issuing Signals via Detection Rules.

**For most cases, the rules defined by Datadog out of the box are sufficient**, but you can add custom rules as needed.

The role does overlap with AWS WAF, but comparing the two, I see differences in placement, the kinds of rules used, and ease of operation.

Personally, I think it works well in a complementary role — catching the suspicious requests that AWS WAF couldn't cover. Strengths it has over AWS WAF include integration with Detection Rules and traces, plus the convenience of intuitive GUI-based operations.

## Detection Rules

**Detection Rules** let you define rules to detect specific threat patterns, making it possible to spot potential attacks.

For example, even if attacks come from a wide range of IP addresses, you can use trace information to pinpoint the attacker and **block the offending User**.

This is a feature unique to Datadog ASM — which assumes Datadog APM is in place — and I get the sense it's going to play a **major role in application security protection going forward**.

By default, Datadog's OOTB Rules are enabled. These use trace information to identify attackers and raise alerts as Signals.

Of course, you can also add your own custom rules.

In addition to raising alerts, you can configure automatic blocking of the attack source.

This means **detection through blocking happens entirely automatically**. Wonderful.

# You Might Also Like

https://zenn.dev/yukionodera/articles/good-about-mise

https://zenn.dev/yukionodera/articles/arc-2-released

https://zenn.dev/yukionodera/articles/how-to-manage-images-with-obsidiann

# Closing Thoughts

If you're trying to decide which application security tool to adopt, I think you can't go wrong starting with this.

I didn't include any screenshots this time, so it may be hard to get the full picture, but the GUI is genuinely convenient and the amount of information it surfaces is impressive — it's a real pleasure to use.

> I just couldn't find time to prep the screenshots.

Although I didn't cover it here, Datadog ASM also offers vulnerability management depending on the language, so if that sounds interesting, definitely check it out.

# References

https://docs.datadoghq.com/security/application_security/threats/protection/

*Subscribe for more Datadog & Observability deep-dives.*
