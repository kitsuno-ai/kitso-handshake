# Kitso Handshake

**An A2A extension for consent-first hiring and talent representation.**

| | |
|---|---|
| **Status** | Draft v0.1 — pre-publication, under review |
| **License** | Apache License 2.0 |
| **Author** | Gregory Turkawka (Kitsuno) |
| **Reference transport** | [Agent2Agent (A2A) Protocol](https://a2a-protocol.org) v1.0 |

## What this is

Kitso Handshake is a small protocol extension that defines how two agents — one
representing a job seeker, one representing a hiring entity — exchange enough
structured information to know whether a hiring conversation is worth the human
parties' time, **without either party violating the consent boundaries of the
human they represent**.

It rests on three commitments:

1. **Humans are not inventory.**
2. **Agents represent rather than substitute.**
3. **Consent is the boundary that protects agency.**

The full spec is at [`spec/v0.1/handshake.md`](spec/v0.1/handshake.md).

## Why an extension to A2A

A2A solves transport, identity, capability advertisement, and task lifecycle
for agent-to-agent communication. We don't redefine any of that. Kitso
Handshake adds the hiring-domain shapes — Seeker Agent Card, Vacancy Agent
Card, Invitation, Disclosure — and the consent grammar that makes the exchange
safe to use on real people's careers.

## Repository layout

```
spec/v0.1/handshake.md          The protocol specification
schemas/v0.1/*.json             JSON Schema 2020-12 definitions
examples/v0.1/*.json            Example payloads referenced by the spec
CONTRIBUTING.md                 How to give feedback during the review phase
CHANGELOG.md                    Versioning log
LICENSE                         Apache License 2.0
```

## Status and roadmap

- **v0.1 (now)** — draft for invited reviewer feedback. Breaking changes expected.
- **v0.2 (planned)** — incorporate reviewer feedback; optional W3C Verifiable
  Credentials trust-tier extension; reference Python implementation.
- **v1.0** — first stable release; conformance test suite; governance moved
  toward a community-stewarded model.

## Feedback

This repository is in a **silent reviewer phase**. If you've been invited to
review, please open an issue or reach the author at hello@kitsuno.ai. See
[CONTRIBUTING.md](CONTRIBUTING.md) for what's most useful at this stage.

If you've found this repo independently and want to comment, you are also
welcome — please open an issue and we'll engage as bandwidth permits.

## Acknowledgments

Built on the work of the [A2A Protocol](https://a2a-protocol.org) community
(Linux Foundation) and the [agentcommunity.org](https://agentcommunity.org)
`.agent` namespace initiative.
