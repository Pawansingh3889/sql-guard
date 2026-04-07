# sql-guard

Fast rule-based SQL linter. 15 rules, zero config, instant results.

Works as a CLI tool, pre-commit hook, and GitHub Action.

## Install

```bash
pip install sql-guard
```

## Usage

```bash
sql-guard check .                          # scan current directory
sql-guard check queries/ --severity error  # errors only
sql-guard check . --fail-fast              # stop on first error
sql-guard check . --disable E002 W008      # skip specific rules
sql-guard list-rules                       # show all 15 rules
```

## What it catches

**Errors (block commit):**

| Rule | What |
|---|---|
| E001 | DELETE without WHERE |
| E002 | DROP without IF EXISTS |
| E003 | GRANT/REVOKE in application code |
| E004 | String concatenation in WHERE (injection risk) |
| E005 | INSERT without column list |

**Warnings:**

| Rule | What |
|---|---|
| W001 | SELECT * |
| W002 | Missing LIMIT on SELECT |
| W003 | Function on indexed column in WHERE |
| W004 | Missing table alias in JOINs |
| W005 | Subquery that could be a JOIN |
| W006 | ORDER BY without LIMIT |
| W007 | Hardcoded values in WHERE |
| W008 | Mixed case keywords |
| W009 | Missing semicolon |
| W010 | Commented-out code |

## Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Pawansingh3889/sql-guard
    rev: v0.1.0
    hooks:
      - id: sql-guard
```

## GitHub Action

```yaml
# .github/workflows/sql-lint.yml
name: SQL Lint
on:
  pull_request:
    paths: ['**/*.sql']

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Pawansingh3889/sql-guard@v1
```

## Pairs with SQL Ops Reviewer

sql-guard handles fast pattern-based checks. For deeper AI-powered analysis, use [SQL Ops Reviewer](https://github.com/Pawansingh3889/sql-ops-reviewer) alongside it:

```
pre-commit: sql-guard (instant, rule-based, catches 80%)
CI:         SQL Ops Reviewer (30s, AI-powered, catches the rest)
```

## License

MIT
