# Engagement pack - what to do this week

This folder holds draft copy for everything outside the code - GitHub Issues
to seed, a pinned Discussion, a Marketplace release checklist, and ready-to-
post announcement copy. Nothing here ships with the package.

## Action checklist (in order)

### Today (30 min)
- [ ] **Enable GitHub Discussions** - repo Settings -> Features -> tick Discussions.
      Create three categories: Q&A, Show and tell, Ideas.
- [ ] **Paste the "Who's using sql-sop?" discussion** -
      copy from [`who-is-using-discussion.md`](who-is-using-discussion.md),
      pin it, and close anyone who posts with a Thanks comment.
- [ ] **Enable the new issue templates** - pushing the files in
      `.github/ISSUE_TEMPLATE/` is enough; GitHub auto-detects them.
- [ ] **Pin one repo Issue** - create "Tracking: v0.5 rule ideas" from the
      good-first-issues list below and pin it too.

### This week (2-3 h)
- [ ] **Seed 10 good-first-issue tickets** - copy each section of
      [`good-first-issues.md`](good-first-issues.md) into a new issue. Tag
      with `good-first-issue`, `help-wanted`, `rule-request`.
- [ ] **Ship the CLI feedback prompt** - code change already applied to
      `sql_guard/reporters/terminal.py`, just confirm it on your branch.
- [ ] **Publish v0.4.1 to GitHub Marketplace** - follow
      [`marketplace-release.md`](marketplace-release.md).
- [ ] **Post the announcement** - pick one channel from
      [`announcement-posts.md`](announcement-posts.md) (LinkedIn is the
      safest-first if you want the low-drama path; Hacker News is higher
      variance).

### This month (6-10 h)
- [ ] **Deploy the Pyodide playground** to GitHub Pages
      (see `playground/README.md`).
- [ ] **Publish the comparison post** at
      [`docs/blog/sqlfluff-vs-sql-sop.md`](../../docs/blog/sqlfluff-vs-sql-sop.md).
      Cross-post to dev.to and Medium.
- [ ] **Submit to newsletters**: Python Weekly, PyCoder's Weekly.
- [ ] **Open a PR against [Awesome Python](https://github.com/vinta/awesome-python)**
      under "Code Analysis" -> "Linters".
- [ ] **Submit a lightning talk CFP**: PyData London, PyData Leeds,
      DDD North.

## Why this order

Discussions + issue templates reduce friction for first-time contributors.
Good-first-issues and the CLI CTA create demand-side signal (people know
what to work on). Marketplace listing and the playground are distribution
multipliers. The blog post and talks are long-tail discovery.

Doing these in order means every step makes the next one easier. Jumping
straight to "post on Hacker News" without issue templates in place wastes
the traffic that lands on the repo.
