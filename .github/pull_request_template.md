<!--
Thanks for contributing to sql-sop! Fill out the sections below so the
maintainer doesn't have to ask. One-line docs fixes can skip most
sections; rule additions should fill everything.
-->

## What changed

<!-- One or two sentences explaining the *why*, not just the *what*. -->

## Related issue

<!-- "Closes #123" or "Relates to #123". -->

## If this adds or changes a rule

- [ ] Rule ID is the next unused one in its family (`E00N` / `W0NN` / `S00N` / `P00N`)
- [ ] Rule class registered in `sql_guard/rules/__init__.py`
- [ ] Fixture line in `tests/fixtures/errors.sql` or `warnings.sql`
- [ ] "Fires on bad SQL" test in `tests/test_rules.py`
- [ ] "Does NOT fire on safe SQL" test (using `tmp_path`)
- [ ] README rule table + Key Numbers count updated
- [ ] Rule is not a removal or rename of an existing rule (breaking change — see `GOVERNANCE.md`)

## Tests

- [ ] `pytest -q` passes
- [ ] `ruff check .` passes

## Checklist

- [ ] One logical change per commit, conventional commit style (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `test:`, `style:`)
- [ ] `CHANGELOG.md` `[Unreleased]` entry if user-facing

## Anything else reviewers should know
