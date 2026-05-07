# Changelog

All notable changes to this protocol will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Once v1.0 is released, this project will adhere to [Semantic Versioning](https://semver.org/).
Until then, breaking changes between minor versions are expected.

## [v0.1] — 2026-05-06

Initial draft, pre-publication, under invited reviewer feedback.

### Added

- Core specification (`spec/v0.1/handshake.md`) defining:
  - Three foundational commitments (humans not inventory, agents represent not
    substitute, consent as boundary).
  - Scope and non-goals for v0.1.
  - Relationship to the Agent2Agent (A2A) Protocol as a typed extension.
  - Core concepts: Principal, Agent, Seeker, Vacancy, Invitation, Disclosure.
  - Schemas for `SeekerAgentCard`, `VacancyAgentCard`, `Invitation`,
    `Disclosure` (informal in spec, formal in `schemas/v0.1/`).
  - Four-tier consent grammar annex (auto-disclosable, confirmation-required,
    human-only, forbidden).
  - Five-tier trust hierarchy annex (domain-verified, .agent-resolved,
    third-party-attested, self-asserted, anonymous).
  - Three worked examples (solo-founder via Telegram, mid-size SaaS via RPO,
    enterprise internal mobility).
- JSON Schema 2020-12 definitions in `schemas/v0.1/`.
- Example payloads in `examples/v0.1/`.

### Known limitations of v0.1

- Compensation negotiation flows are out of scope.
- Reference checks and background verification are out of scope.
- Calendar scheduling is out of scope.
- W3C Verifiable Credentials integration deferred to v0.2.
- Multi-Seeker, multi-Vacancy bulk flows (job fairs, talent pools) deferred.
- No reference implementation yet (planned for v0.2).
