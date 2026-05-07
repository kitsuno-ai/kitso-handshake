# JSON Schemas — v0.1

JSON Schema 2020-12 definitions for the Kitso Handshake protocol.

## Files

| File | Defines |
|---|---|
| `common.json` | Shared enums and reusable types (`ConsentTier`, `TrustTier`, `PrincipalType`, `EmploymentType`, `AgentIdentifier`, `MoneyAmount`, `Geography`, `Authorization`, `Provenance`, ISO format primitives). |
| `seeker-agent-card.json` | The `kitso.handshake.v1` extension block for an A2A AgentCard representing a job seeker. (Spec §4.1) |
| `vacancy-agent-card.json` | The `kitso.handshake.v1` extension block for an A2A AgentCard representing a hiring opportunity. (Spec §4.2) |
| `invitation.json` | Vacancy → Seeker invitation artifact. (Spec §4.3) |
| `disclosure.json` | Seeker → Vacancy response artifact. (Spec §4.4) |

## Conventions

- **Draft:** JSON Schema 2020-12 (`https://json-schema.org/draft/2020-12/schema`).
- **`$id` namespace:** `https://kitsuno.ai/handshake/v0.1/`. The IDs are
  intentionally stable across repository moves.
- **Cross-file `$ref`:** schemas reference `common.json` via relative ref
  (e.g. `"$ref": "common.json#/$defs/TrustTier"`). When resolving from the
  spec namespace, the absolute URI form is `https://kitsuno.ai/handshake/v0.1/common.json#/$defs/TrustTier`.
- **`additionalProperties: false`** on most objects — v0.1 prefers
  conservative validation. The two AgentCard wrappers leave the outer
  envelope open (`additionalProperties: true`) because they live inside an
  A2A AgentCard alongside other extension blocks.

## Validating an example

Python (using [`jsonschema`](https://python-jsonschema.readthedocs.io/) and
[`referencing`](https://referencing.readthedocs.io/)):

```python
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

schemas_dir = Path("schemas/v0.1")
registry = Registry()
for p in schemas_dir.glob("*.json"):
    registry = registry.with_resource(
        uri=p.name,
        resource=Resource.from_contents(json.load(open(p))),
    )

schema = json.load(open(schemas_dir / "invitation.json"))
example = json.load(open("examples/v0.1/invitation.example.json"))

errors = list(Draft202012Validator(schema, registry=registry).iter_errors(example))
assert not errors, errors
```

## Caveats for v0.1

- These schemas validate **structure**, not **policy semantics**. A payload
  that conforms to `invitation.json` is well-formed but may still violate
  the Seeker's `consent_policy` (§5) or be filtered by `trust_tier_required_minimum`
  (§6). Policy enforcement is the agent's responsibility, not the schema's.
- Several free-form `string` fields (`role_family`, `seniority`, `industry`,
  `size_band`, `remote_policy`, `confirmation_method`) are intentionally not
  enumerated at v0.1. v0.2 may introduce controlled vocabularies (e.g. ESCO
  for role/skill, NACE for industry) as optional refinements.
- Scope of `Authorization` (defined in `common.json`) is referenced by the
  spec but not yet wired into the four artifact schemas as a required field.
  This will be tightened in v0.2 once the per-task authorization carrier
  shape is settled.
