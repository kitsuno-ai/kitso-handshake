# Examples — v0.1

Example payloads referenced by the spec (`spec/v0.1/handshake.md`). Each is
valid against the corresponding schema in [`/schemas/v0.1/`](../../schemas/v0.1/)
and is intended both as illustration and as a fixture for any future
conformance test suite.

## Files

| File | Schema | Source |
|---|---|---|
| `seeker-agent-card.example.json` | `seeker-agent-card.json` | Spec §4.1 |
| `vacancy-agent-card.example.json` | `vacancy-agent-card.json` | Spec §4.2 (direct hire) |
| `vacancy-agent-card-rpo.example.json` | `vacancy-agent-card.json` | Spec §7.2 (RPO chain) |
| `vacancy-agent-card-attested.example.json` | `vacancy-agent-card.json` | Spec §7.1 (third-party-attested) |
| `invitation.example.json` | `invitation.json` | Spec §4.3 |
| `disclosure.example.json` | `disclosure.json` | Spec §4.4 |

## Usage

These are illustrative, not normative. Implementations may use them as
starting points for their own fixtures, but should not depend on the exact
identifiers (`inv_20260506_abc123`, `acme.agent`, etc.) — they are placeholders.

If you change a schema in `schemas/v0.1/`, update the corresponding example
in this directory and re-run schema validation.
