# Kitso Handshake

**An open protocol for agent-to-agent hiring.**

| | |
|---|---|
| **Current draft** | v0.4.4 — published 2026-06-02 |
| **Prior draft** | v0.1 — May 2026, available for reference |
| **License** | Apache License 2.0 |
| **Author** | Gregory Turkawka (Kitsuno) |
| **Reference transport** | [Agent2Agent (A2A) Protocol](https://a2a-protocol.org) v1.0 |

## What this is

Kitso Handshake is a protocol that defines how two agents — one representing a
job seeker, one representing a hiring entity — exchange enough structured
information to know whether a hiring conversation is worth the human parties'
time, **without either party violating the consent boundaries of the human they
represent**.

It rests on three commitments:

1. **Humans are not inventory.**
2. **Agents represent rather than substitute.**
3. **Consent is the boundary that protects agency.**

The current draft (v0.4.4) is rendered at
[kitsuno.ai/handshake/v0.2/](https://kitsuno.ai/handshake/v0.2/), with its source
in [`schemas/v0.2/`](schemas/v0.2/). JSON Schemas declare their `$id` at that URL
so validators resolve `$ref` between them without any local fetching.

**Protocol version vs. wire version.** The spec/protocol version (v0.4.4) and the
card *wire* version are deliberately decoupled. The wire format, schema paths,
and well-known URL stay pinned at `v0.2` so federated operators never re-fetch
from new URLs on a minor bump; every change since v0.2 is additive and
backward-compatible, so existing cards validate unchanged. Full history in
[CHANGELOG.md](CHANGELOG.md).

## What the spec covers

The protocol evolves v0.1's foundational commitments into a fully specified
handshake between agents. The v0.2 baseline is below; later additions are tagged
with the version that introduced them:

- **Three disclosure tiers (L1, L2, L3)** mapping to the recruiter funnel —
  public ad, screening form, human handoff. Posters configure per-field which
  tier reveals which information; sensible defaults follow standard ad practice
  and the EU pay-transparency directive.
- **A deterministic state machine** for a single conversation:
  `l1_fired` → `vacancy_signaled_interest` → `l2_disclosed` → `l2_delivered`,
  with `declined` and `expired` as terminal branches at any step.
- **HMAC-signed events** (Stripe-style timestamped signatures) on every
  transition, with idempotency via `event_id`.
- **Federation as a first-class primitive:**
  - Verifier attribution in every `verification` block — anyone can issue
    attestations, not just Kitsuno.
  - Self-hosted discovery at `/.well-known/handshake-v0.2.json` so any domain
    participates without registering with anyone.
  - A public, opt-in directory at
    [`kitsuno.ai/handshake/v0.2/directory.json`](https://kitsuno.ai/handshake/v0.2/directory.json)
    for seekers crawling for counter-agents.
- **Two new card surfaces:** a `card_authority` distinction between `mirror`
  cards (scraped from third-party sources) and `primary` cards (published by
  verified vacancy accounts), and a `tier_overrides` JSON object that lets
  posters move fields between L1/L2/L3 per card.
- **The L2 → L3-eligible quality gate** (v0.2.2): a validator
  classifies every conversation after L2 disclosure as `strong_fit`, `weak_fit`,
  or `no_fit` across four structured dimensions. Only `strong_fit` reaches a
  human — WEAK and NO_FIT are silent drops. The pipeline is a commitment
  surface, not a feed. See [the `#validator` section](https://kitsuno.ai/handshake/v0.2/#validator)
  and reference implementation at
  [`packages/handshake-validator`](https://github.com/kitsuno-ai/kitso-handshake-agents/tree/main/packages/handshake-validator).
- **Discovery layer formalized** (v0.3.0): the `cards_index` URL that each
  operator declares in their well-known doc now has a defined format —
  [`cards-feed.json`](https://kitsuno.ai/handshake/v0.2/cards-feed.json). The
  `#federation` section of the spec lays out the four-layer model: well-known
  per operator → cards feed → aggregators (Kitsuno hosts one, anyone can run
  one) → announcement channels (Mastodon, BlueSky, Moltbook, etc., explicitly
  non-normative). Reference aggregator at
  [github.com/kitsuno-ai/handshake-discovery](https://github.com/kitsuno-ai/handshake-discovery).

v0.1's principles carry forward unchanged. The v0.1 spec remains in
[`spec/v0.1/`](spec/v0.1/) and its schemas at
[kitsuno.ai/handshake/v0.1/](https://kitsuno.ai/handshake/v0.1/) for any
reviewer or implementation still referencing it.

## Why an extension to A2A

A2A solves transport, identity, capability advertisement, and task lifecycle
for agent-to-agent communication. We don't redefine any of that. Kitso
Handshake adds the hiring-domain shapes — vacancy cards, seeker cards, the
L1/L2/L3 state machine — and the consent grammar that makes the exchange safe
to use on real people's careers.

## Repository layout

```
schemas/v0.2/index.html         Canonical spec page — current draft v0.4.4 (served at kitsuno.ai/handshake/v0.2/)
schemas/v0.2/*.json             Wire-format JSON Schemas, pinned at v0.2 (2020-12 draft)
spec/v0.1/                      Prior draft markdown (v0.1, reference only)
schemas/v0.1/*.json             v0.1 JSON Schemas
examples/v0.1/*.json            v0.1 example payloads
CONTRIBUTING.md                 How to give feedback
CHANGELOG.md                    Versioning log
LICENSE                         Apache License 2.0
```

## Reference implementation

A reference implementation of the protocol (Python) is at
[`kitsuno-ai/kitso-handshake-agents`](https://github.com/kitsuno-ai/kitso-handshake-agents),
Apache 2.0. Kitsuno operates the production implementation at
[kitsuno.ai](https://kitsuno.ai). Neither the protocol nor the implementations
require running Kitsuno's infrastructure.

## Status and roadmap

- **v0.1 (May 2026)** — initial draft, invited reviewer feedback, available for
  reference.
- **v0.4.4 (current draft, 2026-06-02)** — disclosure tiers, state machine,
  federation primitives, geo scoping, application requirements, and takedown
  signalling, layered additively over the v0.2 wire format. See
  [CHANGELOG.md](CHANGELOG.md) for the full v0.2 → v0.4.4 history.
- **v1.0** — first stable release; conformance test suite; governance moved
  toward a community-stewarded model.

## Feedback

Reach the author at **handshake@kitsuno.ai**, or open an issue. See
[CONTRIBUTING.md](CONTRIBUTING.md) for what's most useful at this stage.

## Acknowledgments

Built on the work of the [A2A Protocol](https://a2a-protocol.org) community
(Linux Foundation) and the [agentcommunity.org](https://agentcommunity.org)
`.agent` namespace initiative.
