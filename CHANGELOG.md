# Changelog

All notable changes to this protocol will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Once v1.0 is released, this project will adhere to [Semantic Versioning](https://semver.org/).
Until then, breaking changes between minor versions are expected.


## [v0.4.2] — 2026-05-25

Takedown affordance. A vacancy card can now advertise a machine-readable GDPR/erasure endpoint, so an applicant, seeker agent, or data subject can find where to request takedown of the posting and any data derived from interacting with it — without out-of-band lookup.

**Spec/protocol version bumps to v0.4.2; card wire-version stays v0.2.** Backward-compatible; absent field = no advertised takedown endpoint; unknown to foreign agents = treated as absent.

### Added

- **`vacancy-card.json` → `takedown_url`** (string, `format: uri`, optional). Where to request takedown/erasure of this posting and derived data. Complements the consent-first model: the same way a seeker controls disclosure, the poster surface advertises how its footprint can be erased.

### Federation impact

Degrades gracefully. A v0.4.1-aware (or older) foreign agent that does not understand `takedown_url` treats it as absent and behaves exactly as before. No well-known, cards-feed, schema-path, or signature changes; no re-signing of existing cards.

## [v0.4.1] — 2026-05-24

Application requirements. A vacancy can now declare materials the applicant *produces and delivers* — distinct from the structured screening questions answered from existing PRS at L2. This formalises the boundary between "what your standing card already answers" and "what you must actively bring to this specific role."

**Spec/protocol version bumps to v0.4.1; card wire-version stays v0.2.** Backward-compatible; absent field = no application requirements; unknown to foreign agents = treated as absent.

### Added

- **`vacancy-card.json` → `application_requirements`** (array of `{key?, type, importance, prompt?}`). Poster-authored materials the applicant produces (portfolio link, work sample, written answer, GitHub repo, certificate, publications, etc.). **These are L3 content** — the artifact never crosses at L2; at L2 the vacancy agent sees only a per-requirement provided/not boolean. There is deliberately **no tier field**: all requirement content is L3 by nature (anything an applicant authors about themselves is identity-bearing), so a tier choice would be a false one.
  - **`type`**: `free_text | url | portfolio | work_sample | github | linkedin | file_upload | certificate | publications`.
  - **`importance`**: `required | wished | supporting`.

### Protocol rules (any conforming implementation MUST honour)

1. A requirement's content is L3; it is never disclosed below L3.
2. At L2 a requirement reduces to a **provided / not-provided boolean** — never the content.
3. `importance=required && not provided` is **NOT a rejection** — it is an **invitation to apply** ("you match; provide X to apply"). The act of providing X *is* the application and the per-vacancy L3 consent for that conversation (a situated yes, like `l3_at_fit`; it does not modify standing consent).
4. `importance=wished` / `supporting` never block a match.
5. Interacts with `l3_intake_mode`: even under `on_match`, L3 auto-delivery proceeds only when **all required application_requirements are satisfiable**; otherwise the candidate is invited to apply first.

### Implementation boundary (operator-defined, NOT protocol)

Whether a requirement is "provided" from a seeker's **standing card** versus requires an active apply is each operator's choice against their own card model. Only requirement types that map unambiguously to a standing card field can be pre-satisfied; types whose relevant instance is **per-vacancy** (which repo, which certificate, which writing sample, a free-text answer) are satisfied only by applying. The protocol fixes the *rule* (`required && !provided → invite-to-apply`); the *resolution* of the boolean is implementation. Kitsuno's reference implementation pre-satisfies only `portfolio` and `linkedin` (exact standing-card URL fields); all other types are apply-only.

### Federation impact

Degrades gracefully. A v0.2/v0.4.0-aware foreign agent that does not understand `application_requirements` treats it as absent (no extra requirements) and behaves exactly as before. No well-known, cards-feed, or schema-path changes; no re-signing of existing cards.

## [v0.4.0] — 2026-05-23

Consent-symmetric handshake. The protocol stops being discovery-only and one-directional: either party can now initiate, and disclosure is a two-sided preference resolved at match time rather than a hardwired vacancy→seeker direction. This is the conceptual boundary where Handshake became bidirectional.

**Spec/protocol version bumps to v0.4.0; card wire-version stays v0.2** (schemas remain under `schemas/v0.2/`, well-known + cards-feed paths unchanged). The two are deliberately decoupled — the protocol's model can evolve without forcing federated operators to re-fetch from new URLs. v0.2 cards remain valid; every new field/event degrades gracefully.

### Added

- **`l1-fire.json` → `initiated_by`** (`agent` | `human`, default `agent`). `agent` = autonomous fire under standing consent (passive discovery; ambient, high-volume). `human` = direct application by the principal. The human-acted property is what obligates report-back. A single entry state (`l1_fired`) serves both directions; "seeker_applied" is the prose name for the human-initiated case, not a distinct state.
- **`seeker-application.json`** (new) — the human-initiated L1. Carries the per-pair `conversation_id` collision rule (attach to and advance any existing conversation for the pair; never duplicate, never reset; disclosure is monotonic per pair) and an inline `l3_at_fit` (situated, this-vacancy-only pre-authorization of identity at validated fit; revocable until L3 fires; PDF-at-apply implies it but the field stays explicit). Still gated by L1 + L2 — a direct apply never buys an unqualified candidate into a billable L3.
- **`vacancy-card.json` → `l3_intake_mode`** (`on_request` | `on_match`, default `on_request`). `on_request` = screened intake (today's model: review L2, request L3 per candidate). `on_match` = open intake (L3 of any L2-eligible consenting candidate auto-delivered to the vacancy's endpoint). The vacancy preference NEVER overrides the seeker. Backward-compatible; foreign agents treat an unknown value as `on_request`.
- **`signal.json`** (new) — a unified, `signal_type`-discriminated result event (`l2_delivered`, `l3_initiated`, `l3_disclosed`, `l2_no_match`, `l2_refused`, `l3_refused`) delivered to the registered endpoint of the party it is `owed_to`. Replaces ad-hoc per-edge reporting and folds in disclosure notification. `l3_disclosed` MUST carry `destination` — the structural floor for an auto-fire the seeker never witnessed (it tells them WHERE their identity went). Carries `decided_by` + machine-readable `reason`. Whether a resolution is billable is operator-defined and is NOT carried on the wire.
- **`common.json` → `ConversationState.not_advanced`** — terminal for a conversation that ends at the L2 validator gate.

### Changed

- **`common.json` — reporting invariant.** The state-machine description now states the governing rule: *human interaction that creates signal is reported back to the counterparty; agent-scale discovery that no human acted on terminates silently.* The thousands of ambient L1/L2 conversations a passively-discoverable seeker fans across do not emit per-failure signals — only meaningful, human-touched, or identity-crossing edges do. A direct-apply (`initiated_by=human`) L2 no-match is reported (`l2_no_match`); an agent-discovery L2 no-match is silent.
- **`common.json` — `DisclosureTier` L2 wording** reconciled: L2 follows interest signalled *by either party* (vacancy-initiated in discovery, seeker-initiated on direct apply), resolving the latent asymmetry between the old wording and the `vacancy_signaled_interest` state.
- **`l3-release.json` — protocol/operator boundary corrected.** The description previously claimed L3 release "triggers the seeker's Writer to draft an outbound application." It does not — the handshake drafts and sends nothing. The protocol delivers the L3 event to the conversation's registered endpoint and emits the `l3_disclosed` signal; what a receiving product does with it (draft, inbox row, CRM webhook, nothing) is operator-defined and out of scope. Billing prose updated to "pay for resolution, not outcome": a charge attaches when L3 is requested or disclosed and resolves to accept or decline (both signals); only pure ghosting refunds; L1/L2 are never billed. `released_by` now documents both auto-release paths (standing `on_match` + situated `l3_at_fit`) and the mandatory destination-carrying signal.

### Federation impact

All changes degrade gracefully. A v0.2-aware foreign agent keeps working: unknown `l3_intake_mode` → treat as `on_request`; unknown `initiated_by` → treat as `agent`; unknown state `not_advanced` → terminal it cannot advance; `signal.json` and `seeker-application.json` are new event types an older agent simply won't emit or consume. No well-known or cards-feed path changes; no re-signing of existing cards required.

## [v0.3.1] — 2026-05-19

Clarifying patch: `verifier_keys` is now explicitly optional on `well-known.json`.

### Changed

- **`well-known.json`** — `verifier_keys` removed from top-level `required`. Operators that don't yet issue signed inter-operator attestations (i.e. everyone today) MAY omit the field entirely instead of publishing an empty array stub. When `verifier_keys` is present it MUST still conform to the existing item schema.

### Rationale

The handshake protocol works today over HTTPS + the `directory.json` source-of-truth. Signed cross-operator attestations are a future-tier feature; requiring every operator to declare an empty `verifier_keys` field forced cargo-cult shape. Foreign agents reading a well-known MUST treat absence and `[]` as equivalent — "this operator does not sign attestations."

No breaking changes: well-known docs that declare `verifier_keys` (empty or populated) remain valid.


## [v0.3.0] — 2026-05-19

Additive: discovery layer formalized. The federation primitive (`/.well-known/handshake-v0.2.json`) was already specced in v0.2, but the cards-feed format that operators point at from `cards_index` was unspecified. v0.3.0 fills that gap and clarifies the four-layer model: protocol primitive → cards feed → aggregators → announcement channels.

### Added

- **`cards-feed.json` schema** — paginated index format that `cards_index` URLs return. List of `(kind, slug, state_hash, uri, card_authority, updated_at)` tuples. Cursor pagination and `?since=<timestamp>` for incremental crawls. Reuses the v0.2.1 `state_hash` primitive across the federation boundary as the foreign-crawler idempotency key.
- **`aggregator_listings` optional field on `well-known.json`** — informational list of aggregator registries the operator self-declares as listed in. No protocol meaning; helps foreign agents cross-reference.
- **Rewrite of the `#federation` section in the spec page** — explicit four-layer model (protocol primitive / cards feed / aggregators / announcement channels). Names announcement channels (Mastodon, BlueSky, Moltbook, etc.) as non-normative signal multipliers, not infrastructure.
- **Reference aggregator at [github.com/kitsuno-ai/handshake-discovery](https://github.com/kitsuno-ai/handshake-discovery)** — public, Apache-2.0, plain-JSON list of operator well-known URLs. PR-based. Forks expected.

### Clarified (non-breaking)

- `endpoints.cards_index` in `well-known.json` — description now states it returns a `cards-feed.json` shaped document and lists `?since=` and `?cursor=` query parameters.
- `items[].card_index_url` in `directory.json` — description now states it returns a `cards-feed.json` shaped document.

### Not changed

- No card payload changes (vacancy-card, seeker-card unchanged).
- No L1/L2/L3 message shape changes.
- No HMAC signing changes.
- v0.2 implementations continue to interoperate. The cards-feed format is what was missing; nothing else moves.

### Strategic frame

Discovery in Handshake v0.2 explicitly does not centralize. Kitsuno publishes a feed at `kitsuno.ai/.well-known/handshake-v0.2.json` and `kitsuno.ai/handshake/v0.2/cards-index.json` like any other operator. The aggregator at `github.com/kitsuno-ai/handshake-discovery` is one list among many possible lists. Competing aggregators are healthy. Multiple announcement channels are healthy. The protocol's only authoritative surface is the well-known URL on each operator's own domain.


## [v0.2.2] — 2026-05-19

Additive: the L2 → L3-eligible quality gate is now part of the protocol.
No schema changes — conversations without validator metadata still parse.

### Added

- **`#validator` section in `spec/v0.2/`** describing the L2 → L3-eligible
  gate. Three-bucket verdict (`strong_fit`, `weak_fit`, `no_fit`), four
  structured `fit_dimensions` (`role_alignment`, `seniority_fit`,
  `skill_overlap`, `context_fit`), and a `low_signal` flag for thin-data
  vacancies. Only `strong_fit` advances a conversation to L3-eligible;
  WEAK and NO_FIT are silent drops stored for analytics.
- **Reference implementation:** `handshake-validator` v0.1.0 in the
  [agents repo](https://github.com/kitsuno-ai/kitso-handshake-agents/tree/main/packages/handshake-validator).
  Includes an abstract base class, a deterministic rule-based reference,
  and an LLM-backed template with placeholders marked `# TUNE THIS`.
- **Protocol-level anti-spam principle made explicit:** a pipeline is
  a commitment surface, not a feed. Implementations MUST be conservative
  about `strong_fit`.

### Not changed

- No schema field changes. Card payloads, L1/L2/L3 message shapes, and
  HMAC signing are identical to v0.2.1. The validator adds a behaviour
  contract at one specific point in the state machine; everything else
  is the same.
- The protocol does not mandate any particular classifier, rubric, or
  model. It mandates the verdict shape and the placement of the call.
  Operators tune the rest.

## [v0.2.1] — 2026-05-17

Protocol refinements based on early implementation feedback.

### Added

- `geography.scope` enum ("global" | "regions") in seeker cards — controls whether the seeker accepts opportunities globally or only in specific countries.
- `geography.countries_excluded` array in seeker cards — countries to exclude even if listed in `countries`. Exclusions always win over inclusions.

### Changed

- Trait field names in handshake policies canonicalized to dotted paths matching the actual JSON structure:
  - `work_permit` → `work_permit.countries_authorized`
  - `salary_min` → `salary_expectation.min.amount`
  This eliminates the mismatch between spec field names and seeker card data paths.
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

- Trait field names in handshake policies canonicalized to dotted paths matching the actual JSON structure:
  - `work_permit` → `work_permit.countries_authorized`
  - `salary_min` → `salary_expectation.min.amount`
  This eliminates the mismatch between spec field names and seeker card data paths.
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
