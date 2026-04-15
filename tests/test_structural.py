"""Tests for structural rules (S001-S003)."""
from __future__ import annotations


from sql_guard.rules.structural import (
    DeeplyNestedSubquery,
    ImplicitCrossJoin,
    UnusedCTE,
)


class TestImplicitCrossJoin:
    def test_comma_join_detected(self) -> None:
        sql = "SELECT * FROM orders, customers WHERE orders.id = customers.order_id"
        result = ImplicitCrossJoin().check_statement(sql, 1, "test.sql")
        assert result is not None
        assert result.rule_id == "S001"

    def test_explicit_join_passes(self) -> None:
        sql = "SELECT * FROM orders JOIN customers ON orders.id = customers.order_id"
        result = ImplicitCrossJoin().check_statement(sql, 1, "test.sql")
        assert result is None

    def test_single_table_passes(self) -> None:
        sql = "SELECT * FROM orders WHERE id = 1"
        result = ImplicitCrossJoin().check_statement(sql, 1, "test.sql")
        assert result is None


class TestDeeplyNestedSubquery:
    def test_shallow_passes(self) -> None:
        sql = "SELECT * FROM (SELECT id FROM users) sub"
        result = DeeplyNestedSubquery().check_statement(sql, 1, "test.sql")
        assert result is None

    def test_deep_nesting_detected(self) -> None:
        sql = "SELECT * FROM (SELECT * FROM (SELECT * FROM (SELECT 1) a) b) c"
        result = DeeplyNestedSubquery().check_statement(sql, 1, "test.sql")
        assert result is not None
        assert result.rule_id == "S002"
        assert "nested" in result.message.lower()

    def test_no_subquery_passes(self) -> None:
        sql = "SELECT id, name FROM users WHERE active = true"
        result = DeeplyNestedSubquery().check_statement(sql, 1, "test.sql")
        assert result is None


class TestUnusedCTE:
    def test_used_cte_passes(self) -> None:
        sql = "WITH active AS (SELECT * FROM users WHERE active) SELECT * FROM active"
        result = UnusedCTE().check_statement(sql, 1, "test.sql")
        assert result is None

    def test_unused_cte_detected(self) -> None:
        sql = "WITH unused AS (SELECT 1) SELECT * FROM orders"
        result = UnusedCTE().check_statement(sql, 1, "test.sql")
        assert result is not None
        assert result.rule_id == "S003"
        assert "unused" in result.message.lower()

    def test_no_cte_passes(self) -> None:
        sql = "SELECT * FROM orders"
        result = UnusedCTE().check_statement(sql, 1, "test.sql")
        assert result is None
