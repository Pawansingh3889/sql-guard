"""Base rule class — all rules inherit from this."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Finding:
    """A single issue found by a rule."""

    rule_id: str
    severity: str  # "error" | "warning"
    file: str
    line: int
    message: str
    suggestion: str | None = None


class Rule:
    """Base class for all lint rules.

    Rules compile their regex patterns once at init time.
    Single-pass rules check one line at a time.
    Multi-line rules receive the full statement.
    """

    id: str = ""
    name: str = ""
    severity: str = "warning"  # "error" | "warning"
    description: str = ""
    multiline: bool = False  # True if rule needs full statement context

    def check_line(self, line: str, line_number: int, file: str) -> Finding | None:
        """Check a single line. Override for single-pass rules."""
        return None

    def check_statement(self, statement: str, start_line: int, file: str) -> Finding | None:
        """Check a full SQL statement. Override for multi-line rules."""
        return None

    @staticmethod
    def _compile(pattern: str) -> re.Pattern:
        """Compile a regex pattern with IGNORECASE. Called once at init."""
        return re.compile(pattern, re.IGNORECASE)
