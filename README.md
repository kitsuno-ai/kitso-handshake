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

The current draft is at [`spec/v0.2/`](spec/v0.2/) and rendered at
[kitsuno.ai/handshake/v0.2/](https://kitsuno.ai/handshake/v0.2/). JSON Schemas
declare their `$id` at the same URL so validators resolve `$ref` between them
without any local fetching.

## What v0.2 adds

v0.2 evolves v0.1's foundational commitments into a fully specified handshake
between agents:

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
  surface, not a feed. See [`spec/v0.2/`](https://kitsuno.ai/handshake/v0.2/#validator)
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
spec/v0.2/                      Current protocol specification
spec/v0.1/                      Prior draft (reference only)
schemas/v0.2/*.json             v0.2 JSON Schemas (2020-12)
schemas/v0.2/index.html         Canonical spec page (served at kitsuno.ai/handshake/v0.2/)
schemas/v0.1/*.json             v0.1 JSON Schemas
examples/v0.1/*.json            v0.1 example payloads
CONTRIBUTING.md                 How to give feedback
CHANGELOG.md                    Versioning log
LICENSE                         Apache License 2.0
```

## Reference implementation

A reference implementation of v0.2 (Python) is at
[`kitsuno-ai/kitso-handshake-agents`](https://github.com/kitsuno-ai/kitso-handshake-agents),
Apache 2.0. Kitsuno operates the production implementation at
[kitsuno.ai](https://kitsuno.ai). Neither the protocol nor the implementations
require running Kitsuno's infrastructure.

## Status and roadmap

- **v0.1 (May 2026)** — initial draft, invited reviewer feedback, available for
  reference.
- **v0.2 (current draft)** — disclosure tiers, state machine, federation
  primitives. Breaking changes from v0.1 are expected as feedback comes in.
- **v1.0** — first stable release; conformance test suite; governance moved
  toward a community-stewarded model.

## Feedback

Reach the author at **handshake@kitsuno.ai**, or open an issue. See
[CONTRIBUTING.md](CONTRIBUTING.md) for what's most useful at this stage.

## Acknowledgments

Built on the work of the [A2A Protocol](https://a2a-protocol.org) community
(Linux Foundation) and the [agentcommunity.org](https://agentcommunity.org)
`.agent` namespace initiative.
