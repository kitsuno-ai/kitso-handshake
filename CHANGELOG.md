# Changelog

All notable changes to this protocol will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Once v1.0 is released, this project will adhere to [Semantic Versioning](https://semver.org/).
Until then, breaking changes between minor versions are expected.

## [v0.2] — 2026-05-15

Second draft. Expands v0.1's foundational commitments into a fully specified
handshake between agents. Schemas published at
[kitsuno.ai/handshake/v0.2/](https://kitsuno.ai/handshake/v0.2/).

### Added

- Three disclosure tiers (L1, L2, L3) modeled after the recruiter funnel:
  L1 mirrors a public job ad; L2 mirrors application + pre-screen
  (machine-to-machine); L3 is the human handoff with hiring manager identity,
  compensation breakdown, calendar booking, and internal context.
- Deterministic state machine for a conversation:
  `l1_fired` → `vacancy_signaled_interest` → `l2_disclosed` → `l2_delivered`,
  with `declined` and `expired` as terminal branches at any step.
- HMAC-signed events (Stripe-style timestamped signatures) on every transition.
  Receivers deduplicate by `event_id`; signatures older than 5 minutes are
  rejected.
- `card_authority` distinction between `mirror` cards (scraped from third-party
  sources) and `primary` cards (published by verified vacancy accounts).
- `tier_overrides` JSON object on vacancy cards, letting posters demote or
  promote individual fields across L1/L2/L3 (e.g., move salary to L2 in
  jurisdictions where L1 disclosure is restricted, or reveal client identity at
  L1 instead of L3 for non-confidential roles).
- New schemas:
  - `vacancy-card.json` — L1 public surface (replaces `vacancy-agent-card.json`).
  - `seeker-card.json` — L1 seeker surface (replaces `seeker-agent-card.json`).
  - `l1-fire.json` — seeker → vacancy interest signal.
  - `vacancy-signal.json` — vacancy → seeker interest response.
  - `l2-disclosure.json` — seeker → vacancy machine disclosure.
  - `l3-release.json` — vacancy → seeker human handoff trigger.
  - `directory.json` — federation directory.
  - `well-known.json` — self-hosted discovery format.
- Federation primitives:
  - `verifier` attribution field in every `verification` block — any party can
    issue attestations.
  - `/.well-known/handshake-v0.2.json` discovery pattern for self-hosting.
  - Public, paginated, opt-in directory at
    `kitsuno.ai/handshake/v0.2/directory.json`.
- Trust tier `challenge_response_verified` added to the TrustTier enum for
  parties that pass webhook challenge-response in addition to DNS.

### Changed

- Vocabulary shift from `Invitation` / `Disclosure` to `L1 fire` / `L2
  disclosure` / `L3 release` to match the disclosure-tier model.
- Compensation no longer carries a free-form `disclosure_trigger` string;
  instead, the salary fields default to L1 (per EU pay-transparency directive)
  and posters use `tier_overrides` to relocate them.
- `consent_policy` on the seeker card now carries explicit per-stage flags
  (`agent_may_signal_interest_without_human_review`,
  `agent_may_disclose_l2_without_human_review`,
  `agent_may_release_l3_without_human_review`) and a mandatory
  `scope_expires_at` — standing authorizations without expiry remain forbidden.

### Known limitations of v0.2

- Compensation negotiation flows remain out of scope.
- Reference checks and background verification remain out of scope.
- W3C Verifiable Credentials integration deferred to a future minor.
- Multi-Seeker, multi-Vacancy bulk flows (job fairs, talent pools) deferred.

## [v0.1] — 2026-05-06

Initial draft, pre-publication, under invited reviewer feedback. Remains
available at [`spec/v0.1/`](spec/v0.1/) and
[kitsuno.ai/handshake/v0.1/](https://kitsuno.ai/handshake/v0.1/) for any
reviewer or implementation still referencing it.

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
