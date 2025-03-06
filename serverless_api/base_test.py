import os
import requests
import pytest
import dotenv
import logging
from rich.console import Console
from rich.table import Table

# config logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API Key from .env
dotenv.load_dotenv()
NEBULA_API_KEY = os.getenv("NEBULA_API_KEY")

#Api url for text models
TEXT_API_URL = "https://inference.nebulablock.com/v1/chat/completions"

#Api url for image models
IMAGE_API_URL = "https://api.nebulablock.com/api/v1/images/generation"

#Api url for embedding models
EMBEDDING_API_URL =  "https://inference.nebulablock.com/v1/embeddings"
# save
test_results = []

def print_test_report():
    console = Console()
    table = Table(title="Test Report", show_lines=True)

    table.add_column("Test Case", style="cyan", justify="center")
    table.add_column("Result", style="green", justify="center")
    table.add_column("Traceback", style="red", justify="center")

    for test_id, result, error in test_results:
        table.add_row(test_id, result, error if result == "❌ Failed" else "-")

    console.print(table)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    print_test_report()
