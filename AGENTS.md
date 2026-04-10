# AGENTS.md -- sql-guard (sql-sop)

## Project Overview

Rule-based SQL linter published to PyPI as `sql-sop`. Checks `.sql` files for
performance anti-patterns, security risks, and style issues. Ships as a CLI,
pre-commit hook, and GitHub Action.

## Architecture

```
sql_guard/
  cli.py              # Typer CLI entry point (sql-sop check, list-rules, version)
  checker.py           # Core engine: file discovery, statement splitting, rule execution
  rules/
    base.py            # Rule base class and Finding dataclass
    errors.py          # E001-E005 error rules (block commits)
    warnings.py        # W001-W010 warning rules (advisory)
  reporters/
    terminal.py        # Rich terminal output
action.yml             # GitHub Action (composite, installs from PyPI)
pyproject.toml         # Hatchling build, typer + rich dependencies
tests/
  fixtures/            # errors.sql, warnings.sql, clean.sql
  test_rules.py        # 21 tests across 5 test classes
  test_encoding.py     # Encoding edge case tests
```

## Rules

15 rules total: 5 errors (E001-E005), 10 warnings (W001-W010).

- **E001** delete-without-where (multiline)
- **E002** drop-without-if-exists
- **E003** grant-revoke
- **E004** string-concat-in-where (multiline, SQL injection)
- **E005** insert-without-columns
- **W001** select-star
- **W002** missing-limit (multiline)
- **W003** function-on-column (index killer)
- **W004** missing-alias (multiline)
- **W005** subquery-in-where (multiline)
- **W006** orderby-without-limit (multiline)
- **W007** hardcoded-values
- **W008** mixed-case-keywords
- **W009** missing-semicolon (multiline)
- **W010** commented-out-code

## Two-pass checking strategy

The checker runs single-pass (line-by-line) rules first, then multiline
(statement-level) rules. This is intentional for performance -- do not merge
the passes.

## How to run

```bash
pip install sql-sop
sql-sop check path/to/sql/
sql-sop list-rules
```

## Tests

```bash
python -m pytest tests/ -v
```

All 21 tests must pass. Fixture files live in `tests/fixtures/`.

## Conventions

- **Compiled regex**: Every rule compiles its regex patterns once at class
  definition time via `Rule._compile()`. Never use `re.search()` with a raw
  string in a rule -- always pre-compile.
- **ASCII output only**: All terminal output must be ASCII-safe. No Unicode
  symbols or emoji -- Windows cp1252 terminals break on them. Use text markers
  like `[ERROR]` and `[WARN]` instead.
- **Rule base class**: New rules inherit from `Rule` in `rules/base.py`.
  Set `multiline = True` for statement-level rules, `False` for line-by-line.
- **Finding dataclass**: All rule matches return a `Finding` with `rule_id`,
  `severity`, `file`, `line`, `message`, and optional `suggestion`.
- **Severity levels**: Only `"error"` and `"warning"`. Errors exit with code 1.
- **Line length**: 100 chars (ruff config in pyproject.toml).
- **Python**: 3.10+ required. Type hints used throughout.

## Adding a new rule

1. Add the rule class to `rules/errors.py` or `rules/warnings.py`.
2. Follow the ID convention: `E0XX` for errors, `W0XX` for warnings.
3. Register it in `rules/__init__.py` (it feeds `ALL_RULES`).
4. Add a test case in `tests/test_rules.py` with a matching fixture line.
5. Update the rule count assertion in `TestRuleRegistry.test_all_rules_loaded`.

## Build and publish

```bash
pip install hatch
hatch build
hatch publish
```
