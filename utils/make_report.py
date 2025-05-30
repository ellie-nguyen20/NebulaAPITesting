from rich.console import Console
from rich.table import Table
import pytest

test_results = []

def add_result(test_id, passed, error=None):
    test_results.append((
        test_id,
        "✅ Passed" if passed else "❌ Failed",
        error or "-"
    ))

def print_test_report():
    console = Console()
    table = Table(title="Test Report", show_lines=True)
    table.add_column("Test Case", style="cyan", justify="center")
    table.add_column("Result", style="green", justify="center")
    table.add_column("Traceback", style="red", justify="center")

    for test_id, result, error in test_results:
        table.add_row(test_id, result, error)

    console.print(table)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    print_test_report()
