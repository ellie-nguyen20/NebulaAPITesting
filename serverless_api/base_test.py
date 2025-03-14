import os
import sys

import requests
import pytest
import dotenv
import logging

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

# config logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the .env file
file_path = os.path.join(script_dir, "../.env")

# Check if .env file exists
if os.path.exists(file_path):
    load_dotenv(file_path)
    print(".env file loaded")
else:
    print(f".env file {file_path} not found")
    sys.exit()

# Load API Key from .env
dotenv.load_dotenv()
NEBULA_API_KEY = os.getenv("NEBULA_API_KEY")

# Api url for text models
TEXT_API_URL = "https://inference.nebulablock.com/v1/chat/completions"

# Api url for image models
IMAGE_API_URL = "https://api.nebulablock.com/api/v1/images/generation"

# Api url for embedding models
EMBEDDING_API_URL = "https://inference.nebulablock.com/v1/embeddings"
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
