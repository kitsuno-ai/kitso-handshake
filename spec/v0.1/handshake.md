# Kitso Handshake v0.1

**An A2A extension for consent-first hiring and talent representation.**

- **Status:** Draft v0.1 — pre-publication, under review
- **Author:** Gregory Turkawka (Kitsuno)
- **License:** Apache License 2.0
- **Repository:** github.com/kitsuno-ai/kitso-handshake
- **Date:** May 2026
- **Reference transport:** Agent2Agent (A2A) Protocol v1.0

---

## 0. Preamble

This protocol is built on three commitments:

1. **Humans are not inventory.** Talent identification systems that treat candidates as objects to be sourced — by recruiters, by employer agents, by aggregators — produce hiring outcomes that serve everyone except the human whose life is being decided. Consent-first means the human's stance, expressed faithfully, is the precondition for any agent action on their behalf, not an afterthought.

2. **Agents represent rather than substitute.** A handshake between two agents is a handshake between two humans (or human-org pairs) mediated by their representations. The agent's job is to amplify the human's agency in conversations the human cannot personally be present in — not to make decisions the human has not authorized.

3. **Consent is the boundary that protects agency.** Eighty years of talent-agency law has refined what mutual consent looks like in human-talent representation: term-limited, scope-bounded, revocable, non-exclusive by default, with the represented party retaining final say on every binding outcome. This protocol encodes those patterns as machine-readable structure.

This protocol was authored at Kitsuno during 2026 as we designed our agentic-handshake layer. We're publishing it because the consent-first hiring schema deserves to be a community standard rather than vendor IP, and we'd rather build on top of a protocol others can implement than own a closed one alone.

---

## 1. Scope

Kitso Handshake defines:

- **Seeker representation** — how an agent representing a job seeker advertises capability, availability, stance, and constraints, with explicit consent boundaries.
- **Vacancy representation** — how an agent representing a hiring entity (company, RPO, internal-mobility platform) advertises a role, requirements, constraints, and disclosure boundaries.
- **Invitation flow** — the structured exchange by which a Vacancy Agent invites a Seeker Agent's human into a hiring conversation, with consent checkpoints at each escalation step.
- **Consent grammar** — the field-level taxonomy of what is bindable by an agent vs requires human-in-the-loop, what is revocable, what TTL applies, and how scope is expressed.
- **Provenance and trust tiers** — how the receiving party determines the verifiability of a claimed identity (verified domain, `.agent`-resolved, synthesized-from-public-source, anonymous).

It does **not** define:

- Transport (inherited from A2A).
- Identity systems (inherited from A2A's authorization scheme; `.agent` namespace integration noted as one verification path).
- Storage, persistence, or implementation (out of scope by design — the protocol is the contract, not the implementation).
- Compensation, payment, or commission flows between agents and the entities they represent.

## 2. Relationship to A2A

Kitso Handshake is positioned as an extension to the [Agent2Agent (A2A) Protocol](https://a2a-protocol.org), maintained under the Linux Foundation. All transport mechanics — Agent Cards, Tasks, Artifacts, JSON-RPC 2.0 over HTTPS, Server-Sent Events for streaming — are inherited from A2A and not redefined here.

This spec adds:

- A typed **AgentCard extension** declaring `kitso.handshake.v1` capability, with hiring-domain capability fields.
- Two **Task types** (`SeekerInvitation` and `VacancyDisclosure`) with defined lifecycle, consent checkpoints, and Artifact shapes.
- A **consent grammar annex** specifying which Task fields are bindable-by-agent vs require explicit human confirmation.
- A **trust-tier annex** for Agent Card verification.

While v0.1 specifies A2A as the reference transport, the schema and consent grammar defined here are transport-agnostic. Future versions may specify additional transports.

---

## 3. Core concepts

### 3.1 Principal

The human (or human-org pair) the agent represents. Every agent in this protocol has exactly one principal. The principal is the only party who can grant authorization to the agent, modify scope, revoke, or confirm binding outcomes.

### 3.2 Agent

A software representation of a principal that participates in handshakes on the principal's behalf. An agent has:

- A stable identity (`scheme:identifier`, recommended pattern: `kitsuno.agent/u/<id>` or `<domain>.agent/v/<id>`)
- A scoped authorization from its principal (term-limited, scope-bounded, revocable)
- A capability declaration via Agent Card
- A consent policy declaring which actions the agent may take autonomously vs which require principal confirmation

### 3.3 Seeker

A principal looking for opportunities, represented by a Seeker Agent. May be an external job seeker, an employee open to internal mobility, or a contractor open to projects.

### 3.4 Vacancy

A specific opportunity (role, project, internal allocation) represented by a Vacancy Agent. May be authored by a hiring entity directly or synthesized from a public source by a third party (with declared provenance).

### 3.5 Invitation

A structured proposal from a Vacancy Agent to a Seeker Agent that the Seeker's principal consider engaging with the Vacancy. Invitations are the only mechanism by which a Vacancy Agent contacts a Seeker Agent. Invitations carry full context (who, what, why this person, what's at stake at this step) and are presented to the Seeker's principal for human decision before any reply binds.

### 3.6 Disclosure

A structured response from a Seeker Agent to a Vacancy Agent indicating the Seeker's principal's response to an Invitation: accept, decline, request-more-information, propose-alternative-terms. Disclosures may reveal additional Seeker information consented-to by the principal in response to that specific invitation.

---

## 4. Schema (v0.1, informal)

Full JSON Schema definitions in `/schemas/v0.1/`. This section gives the structural overview.

### 4.1 SeekerAgentCard (extension to A2A AgentCard)

```json
{
  "kitso.handshake.v1": {
    "principal_type": "individual",
    "stance": {
      "open_to_invitations": true,
      "active_search": false,
      "ttl": "2026-12-31T23:59:59Z"
    },
    "scope": {
      "role_families": ["software_engineering", "engineering_management"],
      "seniority": ["senior", "staff", "principal"],
      "employment_types": ["permanent", "contract"],
      "geographies": {"countries": ["CH","DE","AT"], "remote_ok": true},
      "languages_for_invitation": ["en", "de"]
    },
    "constraints": {
      "compensation_floor": {"amount": 130000, "currency": "EUR", "period": "year"},
      "company_types_excluded": ["defense", "tobacco"],
      "employment_constraints": ["no_on_call", "no_relocation"]
    },
    "consent_policy": {
      "agent_may_disclose_without_confirmation": ["role_families", "geographies", "seniority"],
      "agent_must_confirm_before_disclosing": ["full_name", "current_employer", "compensation_history"],
      "human_only_contact_for": ["interview_scheduling", "offer_negotiation"]
    },
    "trust_tier_required_minimum": "domain_verified"
  }
}
```

### 4.2 VacancyAgentCard (extension to A2A AgentCard)

```json
{
  "kitso.handshake.v1": {
    "principal_type": "hiring_entity",
    "vacancy": {
      "role_title": "Senior Backend Engineer",
      "role_family": "software_engineering",
      "seniority": "senior",
      "employment_type": "permanent",
      "geography": {"country": "CH", "city": "Zurich", "remote_policy": "hybrid_3_days"},
      "compensation": {
        "disclosed_in_invitation": false,
        "range": {"min": 140000, "max": 180000, "currency": "CHF"},
        "disclosure_trigger": "after_seeker_accepts_invitation"
      },
      "must_haves": ["5y+_backend_experience", "production_distributed_systems"],
      "nice_to_haves": ["rust", "kafka", "mlops"],
      "ttl": "2026-08-01T00:00:00Z"
    },
    "hiring_entity": {
      "name_disclosed_in_invitation": false,
      "name": "Acme Health AG",
      "industry": "healthcare",
      "size_band": "200-500",
      "disclosure_trigger": "after_seeker_accepts_invitation"
    },
    "consent_policy": {
      "agent_may_invite_without_human_review": false,
      "human_in_loop_role": "hiring_manager"
    },
    "provenance": {
      "tier": "domain_verified",
      "domain": "acme.com",
      "agent_dns": "acme.agent"
    }
  }
}
```

### 4.3 Invitation Artifact

```json
{
  "invitation_id": "inv_20260506_abc123",
  "from_vacancy_agent": "acme.agent/v/eng-42",
  "to_seeker_agent": "kitsuno.agent/u/seeker_xyz",
  "issued_at": "2026-05-06T14:22:00Z",
  "expires_at": "2026-05-13T14:22:00Z",
  "match_rationale": {
    "seeker_signals_matched": ["role_family", "seniority", "geography"],
    "vacancy_signals_matched": ["must_haves:4_of_5"],
    "score": 0.87,
    "narrative": "Senior backend role in Zurich, hybrid, matches stance and geography. Must-haves match 4 of 5; nice-to-haves match 1 of 3."
  },
  "disclosed_so_far": {
    "vacancy": ["role_family","seniority","geography","employment_type","must_haves"],
    "hiring_entity": ["industry","size_band"]
  },
  "next_step_at_stake": {
    "step": "accept_invitation",
    "binding": false,
    "what_seeker_reveals_if_accepts": ["full_constraint_list", "language_proficiency"],
    "what_vacancy_reveals_if_accepted": ["hiring_entity_name", "compensation_range"]
  },
  "human_in_loop_required": true
}
```

### 4.4 Disclosure Artifact

```json
{
  "disclosure_id": "disc_20260506_def456",
  "in_response_to": "inv_20260506_abc123",
  "from_seeker_agent": "kitsuno.agent/u/seeker_xyz",
  "issued_at": "2026-05-06T16:08:00Z",
  "principal_decision": "accept",
  "principal_confirmation": {
    "confirmed_at": "2026-05-06T16:07:42Z",
    "confirmation_method": "in_app_explicit"
  },
  "newly_disclosed": {
    "constraints": ["no_on_call","prefers_async_communication"],
    "language_proficiency": [{"language":"en","level":"native"},{"language":"de","level":"C1"}]
  },
  "next_step_requested": "vacancy_agent_disclose_company_and_comp"
}
```

---

## 5. Consent grammar (annex)

Every field in a SeekerAgentCard and VacancyAgentCard, and every step in the Invitation/Disclosure flow, is classified into one of four consent tiers:

| Tier | Definition | Example |
|---|---|---|
| **Auto-disclosable** | Agent may disclose without principal confirmation | Role family, country, seniority |
| **Confirmation-required** | Agent must obtain principal confirmation before disclosing | Full name, current employer, compensation history |
| **Human-only** | Cannot be agent-mediated; requires direct human contact | Interview scheduling, offer negotiation, contract signing |
| **Forbidden** | Cannot be disclosed at all under this AgentCard's policy | Health information, protected class data, personal identifiers in raw form |

Every authorization in the protocol carries:

- **`granted_at`** — timestamp of explicit principal grant
- **`expires_at`** — TTL, mandatory; default 90 days for general scope, 7 days for invitation-specific scope
- **`scope`** — the specific Tasks or fields the authorization covers
- **`revocable`** — always `true`; revocation MUST be respected within 60 seconds of receipt
- **`bindability`** — does this authorization permit the agent to commit on behalf of the principal, or only to negotiate-and-surface

The protocol forbids standing authorizations without expiry. An agent operating with expired authorization MUST cease all action and surface to its principal.

---

## 6. Trust tiers (annex)

When a receiving agent encounters another agent's AgentCard, it MAY apply the following trust tiers:

| Tier | Verification basis | Trust level |
|---|---|---|
| **Domain-verified** | Agent endpoint domain matches a verified entity domain (DNS + TLS + optional DID resolution) | High |
| **`.agent`-resolved** | Agent identity resolves through the `.agent` namespace (per agentcommunity.org) | High |
| **Third-party-attested** | Agent is attested by a known intermediary (e.g., Kitsuno synthesizing a Vacancy Agent from a public HN post, with provenance link) | Medium |
| **Self-asserted** | Agent claims an identity but no external verification | Low |
| **Anonymous** | No identity claimed | Lowest |

A SeekerAgent's `consent_policy.trust_tier_required_minimum` filters which Vacancy Agents may issue invitations. A Vacancy Agent below the required tier MUST be silently ignored (not error-responded to, to prevent enumeration attacks).

---

## 7. Worked examples

### 7.1 Solo founder posting on Telegram

A two-person startup wants to hire a backend engineer. They post in a DACH-tech Telegram channel: *"We're looking for a senior Go engineer, remote-friendly, EU-based, write us at jobs@startup.example."*

A Kitsuno gonzo-layer worker observes the post, classifies it (high confidence: hiring), extracts structure, and synthesizes a transient Vacancy Agent at `kitsuno.agent/synthesized/tg_<channel>/<id>` with:

- `provenance.tier: third_party_attested`
- `provenance.original_source: <telegram_message_url>`
- `provenance.attested_by: kitsuno.agent`

A Seeker Agent matching this stance receives an Invitation. The Invitation is presented to the principal with full provenance: *"This is a synthesized vacancy attested by Kitsuno from a Telegram post. Original source: [link]. Confidence: high. Want me to engage?"* The principal can choose to engage (Disclosure flows back), to engage with reduced trust (decline auto-disclosure of confirmation-required fields), or to dismiss.

If the principal accepts and the Seeker's contact information is revealed, the disclosure is sent **directly to `jobs@startup.example`** because there is no real Vacancy Agent to handshake with — the synthesized agent's job ends at the introduction.

### 7.2 Mid-size SaaS via RPO

A 300-person SaaS company uses an RPO (recruitment process outsourcer). The RPO operates a Vacancy Agent at `rpo-acme.agent/v/saas-eng-42` representing the SaaS company. Because there's a representation chain (RPO → SaaS company), the AgentCard declares this:

```json
"hiring_entity": {
  "represented_via_rpo": true,
  "rpo_name": "Acme RPO",
  "underlying_entity_disclosed": false,
  "disclosure_trigger": "after_seeker_accepts_invitation"
}
```

Invitation flow proceeds normally. Seekers know they're being contacted by an RPO representing an undisclosed company. They can choose to accept on those terms or require disclosure of the underlying company first as a condition of engagement.

### 7.3 Enterprise internal mobility

A large pharma company runs internal mobility through a federated A2A mesh inside its corporate boundary. Externally, one endpoint exists: `pharma.agent/internal-mobility`. Internally, it routes to ~200 project-specific Vacancy Agents (one per active internal project posting).

An employee's Seeker Agent is registered at `pharma.agent/u/<emp_id>` with `principal_type: employee` and stance `open_to_internal_mobility: true`. The employee's AgentCard is **separate from their HR profile** — the employee owns it, the company hosts it. The company cannot inspect the employee's Seeker stance directly; it can only issue invitations and observe responses.

Project lead's Vacancy Agent finds matches. Invitations flow to employee Seeker Agents. Each employee receives, in their work tooling, a presentation of the invitation with full project context, and chooses to accept / decline / ask-more / propose-alternative — *with the same agency they would have for an external opportunity*. The protocol is identical; only the deployment is internal.

This is the case the protocol was partly designed for, and it is also the structurally cleanest one because the relationship between Seeker and Vacancy already exists — the friction is just discovery and consent-respecting opt-in.

---

## 8. Out of scope for v0.1

- Compensation negotiation flows. The protocol stops at "company has disclosed range, seeker has been informed." Actual offer negotiation is human-only.
- Reference checks and background verification. These are downstream of handshake completion and protocol-irrelevant.
- Calendar scheduling. A complementary protocol problem; out of scope here.
- Verifiable credentials integration (W3C VC). Anticipated in v0.2 as an optional trust-tier extension.
- Multi-Seeker, multi-Vacancy bulk flows (job fairs, talent pools). v0.1 is point-to-point only.

---

## 9. Versioning and governance

v0.1 is a draft for community review. Breaking changes are expected before v1.0.

The protocol is published under Apache License 2.0 and may be implemented, extended, or forked by anyone. Reference implementations and conformance tests will be published alongside v1.0.

Long-term governance is intentionally undefined at v0.1. If the spec gathers community traction, governance will move toward a model similar to A2A's Linux Foundation stewardship. Until then, the spec is maintained by Kitsuno with input from acknowledged reviewers.

---

## 10. Acknowledgments

The author thanks the following reviewers for their feedback on pre-publication drafts. Inclusion in this list does not imply endorsement of the final spec by the reviewer or their affiliated institutions.

- *[placeholder — to be populated post-review]*
- *[placeholder]*
- *[placeholder]*

The author also acknowledges the [Agent2Agent (A2A) Protocol](https://a2a-protocol.org) community, the [agentcommunity.org](https://agentcommunity.org) initiative, and the broader open-protocol ecosystem on whose work this extension depends.

---

## 11. Methodology note

This spec was drafted at Kitsuno during 2026 by Gregory Turkawka, with thinking-partnership from Claude (Anthropic) during design and drafting sessions. All commitments, decisions, and authorial responsibility rest with the human author.

---

## Appendix A — Reference: A2A protocol

[Link to A2A v1.0 specification at a2a-protocol.org]

## Appendix B — JSON Schemas

See `/schemas/v0.1/` in the repository.

## Appendix C — Reference implementation

See `/reference/python/` (planned for v0.2).
