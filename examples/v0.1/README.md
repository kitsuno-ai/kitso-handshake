# Examples — v0.1

Example payloads referenced by the spec. Every file in this directory is
verified to validate against its corresponding schema in `schemas/v0.1/` at
build time.

## Files

| File | Schema | Source |
|---|---|---|
| `seeker-agent-card.example.json` | `seeker-agent-card.json` | Spec §4.1 |
| `vacancy-agent-card.example.json` | `vacancy-agent-card.json` | Spec §4.2 |
| `invitation.example.json` | `invitation.json` | Spec §4.3 |
| `disclosure.example.json` | `disclosure.json` | Spec §4.4 |
| `vacancy-agent-card.synthesized-from-telegram.example.json` | `vacancy-agent-card.json` | Spec §7.1 (Telegram-synthesized vacancy) |

## Usage

These are illustrative, not normative. Implementations may use them as
starting points for their own fixtures, but should not depend on the exact
identifiers (`inv_20260506_abc123`, `acme.agent`, etc.) — they are placeholders.

If you change a schema in `schemas/v0.1/`, update the corresponding example
in this directory and re-run schema validation.
