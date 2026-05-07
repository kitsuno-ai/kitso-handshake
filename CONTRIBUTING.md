# Contributing to Kitso Handshake

Thanks for your interest in this protocol. Kitso Handshake is currently in a
**silent reviewer phase** before formal publication of v0.1, so the kind of
feedback that's most useful right now is different from what would be useful
once the spec is stable.

## What's most useful at v0.1

In rough order of value:

1. **Conceptual challenges to the consent grammar.** Are there field tiers
   missing from the four-tier consent taxonomy in §5? Are any of the
   "auto-disclosable" defaults wrong in a jurisdiction or industry you know
   well? Is there a class of human-only field we've omitted?
2. **Missing worked examples.** §7 covers solo-founder, mid-size-via-RPO, and
   enterprise-internal-mobility. If your domain is meaningfully different
   (academic hiring, public-sector, contractor marketplaces, talent agencies
   in entertainment or athletics), tell us where the protocol breaks.
3. **Trust-tier ambiguities.** §6 defines five tiers. If you can construct a
   case where the right tier is genuinely unclear, that's a spec bug.
4. **Schema correctness.** Field names, types, required-vs-optional, enum
   values. Reproducible examples preferred.
5. **A2A integration concerns.** If you work on A2A, please flag anything in
   the extension that conflicts with A2A's evolving direction.

## What's less useful right now

- **Editorial nits, prose rewriting, formatting suggestions.** We'll do an
  editing pass after the conceptual review settles.
- **Adoption strategy or marketing input.** Out of scope at the spec level.
- **Implementation requests.** Reference implementations come at v0.2.

## How to submit feedback

- **Open a GitHub issue** for anything you'd be comfortable discussing in
  public. Use the `feedback` label.
- **Email hello@kitsuno.ai** for anything sensitive (e.g. industry-specific
  consent issues you'd rather not air publicly until they're resolved).
- **Do not open pull requests against `spec/v0.1/handshake.md` yet.** We're
  collecting feedback first; PRs will be welcome after v0.1 is published.

## Code of conduct

Standard: be substantive, be specific, assume good faith, focus on the work.
Personal attacks or harassment will get you removed without ceremony.

## Attribution

Reviewers who provide substantive feedback may be acknowledged in §10 of the
spec, with consent. Acknowledgment is not endorsement of the final spec.
