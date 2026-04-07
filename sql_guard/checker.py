"""Core checker — orchestrates file discovery, scanning, and rule execution."""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from pathlib import Path

from sql_guard.rules import get_rules
from sql_guard.rules.base import Finding, Rule


@dataclass
class CheckResult:
    """Aggregated result of checking one or more files."""

    findings: list[Finding] = field(default_factory=list)
    files_checked: int = 0
    files_with_issues: int = 0
    duration_seconds: float = 0.0

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


SKIP_PATTERNS = {"*.min.sql", "*.bak"}


def discover_files(paths: list[str], ignore: list[str] | None = None) -> list[Path]:
    """Find all .sql files in the given paths, respecting ignore patterns."""
    sql_files: list[Path] = []
    ignore_set = set(ignore or [])

    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix == ".sql":
            sql_files.append(path)
        elif path.is_dir():
            for f in path.rglob("*.sql"):
                rel = str(f.relative_to(path))
                if any(f.match(pat) for pat in SKIP_PATTERNS):
                    continue
                if any(part in rel for part in ignore_set):
                    continue
                sql_files.append(f)

    return sorted(sql_files)


def _split_statements(content: str) -> list[tuple[int, str]]:
    """Split SQL content into statements with their starting line numbers.

    Returns list of (start_line, statement_text).
    """
    statements: list[tuple[int, str]] = []
    current: list[str] = []
    start_line = 1

    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            if not current:
                start_line = i + 1
            else:
                current.append(line)
            continue

        if not current:
            start_line = i
        current.append(line)

        if stripped.endswith(";"):
            statements.append((start_line, "\n".join(current)))
            current = []
            start_line = i + 1

    # Handle last statement without semicolon
    if current:
        statements.append((start_line, "\n".join(current)))

    return statements


def _file_hash(path: Path) -> str:
    """Fast hash of file content for caching."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def check_file(
    path: Path,
    rules: list[Rule],
    fail_fast: bool = False,
) -> list[Finding]:
    """Check a single SQL file against all rules.

    Uses two-pass strategy:
    1. Single-pass rules: line-by-line (fast)
    2. Multi-line rules: statement-level (only if needed)
    """
    findings: list[Finding] = []
    content = path.read_text(encoding="utf-8")
    file_str = str(path)

    single_pass_rules = [r for r in rules if not r.multiline]
    multi_line_rules = [r for r in rules if r.multiline]

    # Pass 1: line-by-line rules
    for line_num, line in enumerate(content.splitlines(), 1):
        for rule in single_pass_rules:
            finding = rule.check_line(line, line_num, file_str)
            if finding:
                findings.append(finding)
                if fail_fast and finding.severity == "error":
                    return findings

    # Pass 2: statement-level rules
    if multi_line_rules:
        statements = _split_statements(content)
        for start_line, statement in statements:
            for rule in multi_line_rules:
                finding = rule.check_statement(statement, start_line, file_str)
                if finding:
                    findings.append(finding)
                    if fail_fast and finding.severity == "error":
                        return findings

    return findings


def check(
    paths: list[str],
    severity: str = "warning",
    fail_fast: bool = False,
    disabled_rules: set[str] | None = None,
    ignore: list[str] | None = None,
) -> CheckResult:
    """Run all rules against discovered SQL files.

    Args:
        paths: Files or directories to check.
        severity: Minimum severity to report ("error" or "warning").
        fail_fast: Stop after first error.
        disabled_rules: Set of rule IDs to skip.
        ignore: Path patterns to ignore.

    Returns:
        CheckResult with all findings.
    """
    t0 = time.perf_counter()
    rules = get_rules(disabled_ids=disabled_rules)
    sql_files = discover_files(paths, ignore=ignore)

    result = CheckResult()
    result.files_checked = len(sql_files)

    for path in sql_files:
        file_findings = check_file(path, rules, fail_fast=fail_fast)

        # Filter by severity
        if severity == "error":
            file_findings = [f for f in file_findings if f.severity == "error"]

        if file_findings:
            result.files_with_issues += 1
            result.findings.extend(file_findings)

            if fail_fast and any(f.severity == "error" for f in file_findings):
                break

    result.duration_seconds = round(time.perf_counter() - t0, 3)
    return result
