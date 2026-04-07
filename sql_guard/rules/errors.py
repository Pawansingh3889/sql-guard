"""Error rules (E001-E005) -- these block commits."""

from __future__ import annotations

from sql_guard.rules.base import Finding, Rule


class DeleteWithoutWhere(Rule):
    """E001: DELETE statement without WHERE clause."""

    id = "E001"
    name = "delete-without-where"
    severity = "error"
    description = "DELETE without WHERE affects all rows in the table"
    multiline = True

    _pattern = Rule._compile(r"\bDELETE\s+FROM\s+\S+")
    _has_where = Rule._compile(r"\bWHERE\b")

    def check_statement(self, statement: str, start_line: int, file: str) -> Finding | None:
        if self._pattern.search(statement) and not self._has_where.search(statement):
            return Finding(
                rule_id=self.id,
                severity=self.severity,
                file=file,
                line=start_line,
                message="DELETE without WHERE clause -- this will delete all rows",
                suggestion="Add a WHERE clause to limit affected rows",
            )
        return None


class DropWithoutIfExists(Rule):
    """E002: DROP TABLE/VIEW without IF EXISTS."""

    id = "E002"
    name = "drop-without-if-exists"
    severity = "error"
    description = "DROP without IF EXISTS will fail if the object doesn't exist"
    multiline = False

    _pattern = Rule._compile(r"\bDROP\s+(TABLE|VIEW|INDEX|SCHEMA|DATABASE)\s+(?!IF\s+EXISTS\b)")

    def check_line(self, line: str, line_number: int, file: str) -> Finding | None:
        if self._pattern.search(line):
            return Finding(
                rule_id=self.id,
                severity=self.severity,
                file=file,
                line=line_number,
                message="DROP without IF EXISTS",
                suggestion="Use DROP TABLE IF EXISTS to avoid errors",
            )
        return None


class GrantRevoke(Rule):
    """E003: GRANT or REVOKE in application code."""

    id = "E003"
    name = "grant-revoke"
    severity = "error"
    description = "Privilege changes should not be in application SQL"
    multiline = False

    _pattern = Rule._compile(r"^\s*(GRANT|REVOKE)\b")

    def check_line(self, line: str, line_number: int, file: str) -> Finding | None:
        if self._pattern.search(line):
            return Finding(
                rule_id=self.id,
                severity=self.severity,
                file=file,
                line=line_number,
                message="GRANT/REVOKE in application code",
                suggestion="Manage permissions through migration scripts or DBA tools",
            )
        return None


class StringConcatInWhere(Rule):
    """E004: String concatenation in WHERE clause -- SQL injection risk."""

    id = "E004"
    name = "string-concat-in-where"
    severity = "error"
    description = "String concatenation in WHERE creates SQL injection risk"
    multiline = True

    _where = Rule._compile(r"\bWHERE\b")
    _concat = Rule._compile(r"\+\s*@|\+\s*'|'\s*\+|\|\|")

    def check_statement(self, statement: str, start_line: int, file: str) -> Finding | None:
        if self._where.search(statement) and self._concat.search(statement):
            return Finding(
                rule_id=self.id,
                severity=self.severity,
                file=file,
                line=start_line,
                message="String concatenation in WHERE clause -- SQL injection risk",
                suggestion="Use parameterised queries: WHERE id = @id",
            )
        return None


class InsertWithoutColumns(Rule):
    """E005: INSERT without explicit column list."""

    id = "E005"
    name = "insert-without-columns"
    severity = "error"
    description = "INSERT without column list breaks when schema changes"
    multiline = False

    _pattern = Rule._compile(r"\bINSERT\s+INTO\s+\S+\s+VALUES\b")

    def check_line(self, line: str, line_number: int, file: str) -> Finding | None:
        if self._pattern.search(line):
            return Finding(
                rule_id=self.id,
                severity=self.severity,
                file=file,
                line=line_number,
                message="INSERT without explicit column list",
                suggestion="Specify columns: INSERT INTO table (col1, col2) VALUES ...",
            )
        return None
