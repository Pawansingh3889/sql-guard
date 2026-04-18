# Changelog

All notable changes to **sql-sop** are logged here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
sql-sop uses [Semantic Versioning](https://semver.org/).

Rule removals and rule ID renames are **breaking changes** that require
a deprecation window (see `GOVERNANCE.md` § Scope discipline).

## [Unreleased]

### Added
- **Contributor paperwork** — `NOTICE`, `GOVERNANCE.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md` with the "Adding a new rule"
  walkthrough. Issue templates for bug reports and feature requests,
  PR template with the rule-addition checklist, CODEOWNERS routing
  reviews, first-contributor welcome workflow, PR-title validator.

### Changed
- **Licence stays MIT, deliberately.** `NOTICE` explains: the package
  has been consumed as MIT on PyPI since v0.1.0; relicensing silently
  is a breaking change for downstream users whose compliance pipelines
  are configured around the current licence.

## [0.4.0] - 2026-04

### Added
- **libCST-based Python scanner** — `sql-sop check --include-python`
  walks Python source via libCST (install with `pip install "sql-sop[python]"`).
  Four new rules (`P001`–`P004`) catch SQL injection in `.execute()`,
  `.read_sql()`, and `sqlalchemy.text(...)` calls:
  - P001 `fstring-in-execute` — `cursor.execute(f"... {user_input}")`
  - P002 `concat-in-execute` — `cursor.execute("..." + user_input)`
  - P003 `format-in-execute` — `.format()` / `%` interpolation
  - P004 `bare-variable-in-execute` — `cursor.execute(query)`

### Added (SQL rules)
- **E006 `update-without-where`** — silent twin of E001. Catches
  `UPDATE table SET col = 'x'` with no `WHERE` before it rewrites every
  row. Registered in `ALL_RULES`, fixture line in `tests/fixtures/errors.sql`,
  two tests (fires + does-not-fire-when-WHERE-present).

### Fixed
- **Pattern 16 word-boundary** — `(product|plu).*waste` was greedy-matching
  `production...waste`. Tightened to `\b(product|plu)\b.*waste`.

## [0.3.0] - 2026-04

### Added
- **Structural rules (S001–S003)** via sqlparse AST:
  - S001 `implicit-cross-join` — missing `ON` / `USING` in `JOIN`
  - S002 `deeply-nested-subquery` — subqueries beyond 3 levels deep
  - S003 `unused-cte` — `WITH` clause defined but never referenced
- **Fluent API** — `SqlGuard().enable("E001").scan("DELETE FROM users")`

## [0.2.0]

### Added
- Pre-commit hook + GitHub Action distributions
- Initial CLI with `check` command

## [0.1.0]

### Added
- First release. Core rule engine with 5 errors + 10 warnings.
