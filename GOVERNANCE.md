# sql-sop governance

A small, focused SQL linter published on PyPI. Governance matches the
project's scope — short, explicit about the PyPI-stability bar.

## Roles

### Maintainer

Currently: **[@Pawansingh3889](https://github.com/Pawansingh3889)**.

Final decision on:

- merges to `main`
- PyPI releases
- rule additions / removals
- the licence (see `NOTICE` for why MIT is deliberately kept)
- this governance document

Commits to:

- replying to issues and PRs within **7 calendar days**
- merging green, in-scope PRs within **14 calendar days**
- batching PyPI releases so downstream users don't see a new
  version every week

### Triage collaborator

Granted to contributors with three merged, in-scope PRs. Can label,
assign, and close duplicate / off-topic issues. Cannot merge, publish
to PyPI, or change repository settings.

### Contributor

Anyone who files an issue or opens a PR.

## Decisions

Rule additions and rule tightenings — one maintainer approval on the
PR. Every new rule needs a test fixture demonstrating it fires on
bad SQL and does not fire on safe SQL.

Rule removals, rule ID renames, default-severity changes — start as
an **issue with a proposal**, because these break downstream pre-commit
configurations. Proposal template:

1. why the rule is being removed or changed
2. what replaces it (if anything)
3. a deprecation window — usually one minor version

### Architecture Decision Records (ADRs)

Proposals that change *how* sql-sop works (new regex engine, new parser
backend, new distribution format) are labelled **`ADR`** on the issue
so they stay easy to find later. Pattern borrowed from Camila Maia's
ScanAPI talk (PyCon DE 2026). After discussion lands on a decision, a
follow-up issue with the task breakdown references back to the ADR, and
the ADR issue stays open in an archived state as the record of "why we
did it this way."

## Issue assignment (first-PR-wins)

1. Comment "I'd like to work on this" — 7-day soft claim.
2. Expire silently after 7 days; anyone may pick up.
3. If two PRs land, the first to pass CI and request review wins.

## Scope discipline

Hard lines:

- **Fast and rule-based, not AI.** sql-sop stays a pure-Python
  regex + sqlparse checker. For AI review, pair with sql-ops-reviewer.
- **Low false-positive rate.** A rule that fires on safe SQL costs
  every downstream user minutes of triage. Prefer "don't fire" to
  "fire and suggest".
- **Stable rule IDs.** `E001`, `W001`, etc. are public API. They
  appear in users' pre-commit configs, GitHub Actions configs, and
  CI badges. Don't renumber.
- **Tests per rule.** No rule lands without at least one "fires on
  bad SQL" test and one "does not fire on safe SQL" test.

## Release cadence

Batched releases to PyPI via the trusted-publishing workflow. Target
cadence: monthly if there are changes, otherwise when justified.

- SemVer: major.minor.patch
- Breaking changes (rule removal, severity change) bump the minor
  version and come with one minor of deprecation notice
- Stable rule additions bump the minor version
- Bug fixes bump the patch version

`README.md` carries a "Key Numbers" block with the current version
and count; keep that honest.

## Licensing

MIT, deliberately. See `NOTICE` for the reasoning — relicensing a
published PyPI package is a breaking change for downstream users
configured around a specific licence, so any relicense conversation
is a major-version (v1.0) event with an explicit migration notice.

## Security

See `SECURITY.md`. Security issues route via private advisory.

## Changes to this document

Via PR from the maintainer. Community input welcome in issues.
