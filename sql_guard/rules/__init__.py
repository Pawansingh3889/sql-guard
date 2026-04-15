"""Rule registry — auto-discovers all rules."""

from __future__ import annotations

from sql_guard.rules.base import Rule
from sql_guard.rules.errors import (
    DeleteWithoutWhere,
    DropWithoutIfExists,
    GrantRevoke,
    InsertWithoutColumns,
    StringConcatInWhere,
)
from sql_guard.rules.warnings import (
    FunctionOnIndexedColumn,
    HardcodedValues,
    MissingLimit,
    MissingSemicolon,
    MissingTableAlias,
    MixedCaseKeywords,
    OrderByWithoutLimit,
    SelectStar,
    SubqueryCouldBeJoin,
    CommentedOutCode,
)
from sql_guard.rules.structural import (
    DeeplyNestedSubquery,
    ImplicitCrossJoin,
    UnusedCTE,
)

ALL_RULES: list[Rule] = [
    # Errors (E001-E005)
    DeleteWithoutWhere(),
    DropWithoutIfExists(),
    GrantRevoke(),
    StringConcatInWhere(),
    InsertWithoutColumns(),
    # Warnings (W001-W010)
    SelectStar(),
    MissingLimit(),
    FunctionOnIndexedColumn(),
    MissingTableAlias(),
    SubqueryCouldBeJoin(),
    OrderByWithoutLimit(),
    HardcodedValues(),
    MixedCaseKeywords(),
    MissingSemicolon(),
    CommentedOutCode(),
    # Structural (S001-S003)
    ImplicitCrossJoin(),
    DeeplyNestedSubquery(),
    UnusedCTE(),
]


def get_rules(enabled_ids: set[str] | None = None, disabled_ids: set[str] | None = None) -> list[Rule]:
    """Return filtered list of rules based on config."""
    rules = ALL_RULES
    if enabled_ids:
        rules = [r for r in rules if r.id in enabled_ids]
    if disabled_ids:
        rules = [r for r in rules if r.id not in disabled_ids]
    return rules
