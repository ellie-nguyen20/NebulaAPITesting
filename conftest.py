import pytest
import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

def load_config(env):
    with open("config.yaml", "r") as file:
        config_data = yaml.safe_load(file)
    if env not in config_data:
        raise ValueError(f"Unknown environment: {env}")
    return config_data[env]

def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="staging", help="Choose environment: staging or production"
    )
    parser.addoption(
        "--key", action="store", default="personal", help="Choose API key type: personal or team"
    )

@pytest.fixture(scope="module")
def config(pytestconfig):
    load_dotenv(override=True)

    env = pytestconfig.getoption("env")
    key_type = pytestconfig.getoption("key")

    # Load base_url and related URLs from YAML file
    config_data = load_config(env)

    # Get API key from environment variable
    env_var_name = f"{env.upper()}_{key_type.upper()}_KEY"
    api_key = os.getenv(env_var_name)
    if not api_key:
        raise ValueError(f"Missing API key in environment variable: {env_var_name}")

    # Add api_key to config_data
    config_data["api_key"] = api_key

    return config_data
