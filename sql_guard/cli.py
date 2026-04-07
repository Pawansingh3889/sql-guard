"""sql-guard CLI — check SQL files for common issues."""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from sql_guard import __version__
from sql_guard.checker import check
from sql_guard.reporters.terminal import print_result
from sql_guard.rules import ALL_RULES

app = typer.Typer(
    name="sql-guard",
    help="Fast rule-based SQL linter.",
    no_args_is_help=True,
)
console = Console()


@app.command("check")
def check_cmd(
    paths: list[str] = typer.Argument(default=None, help="Files or directories to check."),
    severity: str = typer.Option("warning", "--severity", "-s", help="Minimum severity: error or warning."),
    fail_fast: bool = typer.Option(False, "--fail-fast", help="Stop after first error."),
    disable: Optional[list[str]] = typer.Option(None, "--disable", "-d", help="Rule IDs to disable."),
) -> None:
    """Check SQL files for common issues."""
    if not paths:
        paths = ["."]

    disabled = set(disable) if disable else None
    result = check(paths, severity=severity, fail_fast=fail_fast, disabled_rules=disabled)
    print_result(result)

    if result.error_count > 0:
        raise typer.Exit(code=1)


@app.command("list-rules")
def list_rules() -> None:
    """List all available lint rules."""
    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    table.add_column("ID")
    table.add_column("Severity")
    table.add_column("Name")
    table.add_column("Description", style="dim")

    for rule in ALL_RULES:
        sev = "[red]error[/red]" if rule.severity == "error" else "[yellow]warning[/yellow]"
        table.add_row(rule.id, sev, rule.name, rule.description)

    console.print(table)


@app.command()
def version() -> None:
    """Show version."""
    console.print(f"sql-guard {__version__}")
