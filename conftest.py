import pytest
import yaml
import os
from dotenv import load_dotenv
import json
import requests
from pathlib import Path
from api_clients.credit_api import CreditsAPI

# Load environment variables from .env file if exists
load_dotenv()

# Import fixtures from fixtures module
from fixtures.auth_token import auth_token, user_credentials

# Path to users.json
USERS_FILE = Path(__file__).parent / "data" / "users.json"

# Load all users at pytest startup
with open(USERS_FILE, "r", encoding="utf-8") as f:
    USERS = json.load(f)

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
    parser.addoption(
        "--user",
        action="store",
        default=None,
        help="User name from users.json to use (e.g., Owner, Admin, Member1)"
    )

@pytest.fixture(scope="session")
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

    # Add backward compatibility aliases for new config structure
    if "base_url" in config_data and "model_base_url" in config_data:
        # For backward compatibility, keep old keys
        config_data["image_base_url"] = config_data.get("image_generation_url", "")
        config_data["embedding_base_url"] = config_data.get("embedding_url", "")
        config_data["portal_base_url"] = config_data.get("base_url", "")  # New structure
        
        # Add full endpoint URLs if not present
        if "chat_completions_url" not in config_data:
            config_data["chat_completions_url"] = f"{config_data['model_base_url']}/v1/chat/completions"
        if "image_generation_url" not in config_data:
            config_data["image_generation_url"] = f"{config_data['base_url']}/api/v1/images/generation"

    return config_data

@pytest.fixture(scope="session")
def selected_user(pytestconfig):
    """
    Returns the selected user info based on CLI option or defaults to the first user.
    """
    user_name = pytestconfig.getoption("--user")

    if user_name:
        if user_name in USERS:
            chosen = USERS[user_name]
            print(f"[pytest] Using user from CLI: {user_name} -> {chosen['email']}")
            return chosen
        else:
            pytest.exit(f"[pytest] ❌ User '{user_name}' not found in {USERS_FILE}")

    # Fallback to the first user in the JSON
    first_user_name = next(iter(USERS))
    chosen = USERS[first_user_name]
    print(f"[pytest] No --user provided, using default: {first_user_name} -> {chosen['email']}")
    return chosen

@pytest.fixture(scope="session")
def auth_token(config, selected_user):
    """Get authentication token once for entire test session"""
    base_url = config["base_url"]
    
    try:
        print(f"Login once for entire test session with user: {selected_user['email']}")
        payload = {"username": selected_user["email"], "password": selected_user["password"]}
        resp = requests.post(f"{base_url}/login", data=payload, timeout=10)
        
        if resp.status_code == 200:
            response_data = resp.json()
            if "data" in response_data and "jwtToken" in response_data["data"]:
                token = response_data["data"]["jwtToken"]
                print(f"✅ Login successful - token will be reused for all tests")
                
                # Trả về tuple (token, None, []) để giữ backward compatibility
                return token, None, []
            else:
                print(f"Login response missing jwtToken: {resp.text}")
        else:
            print(f"Login failed: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print(f"Login error: {e}")
    
    raise Exception(f"Failed to login. Status: {resp.status_code}, Response: {resp.text}")


def _select_best_api_key(api_keys):
    """
    Logic chọn API key tốt nhất từ danh sách.
    Ưu tiên: Personal keys (team: null) > Active keys > Keys có team
    """
    if not api_keys:
        return None
    
    # Lọc active keys (status = 1)
    active_keys = [key for key in api_keys if key.get("status") == 1]
    
    if not active_keys:
        print("⚠️ No active API keys found")
        return None
    
    # Ưu tiên personal keys (team: null) - đây là keys cá nhân
    personal_keys = [key for key in active_keys if not key.get("team")]
    team_keys = [key for key in active_keys if key.get("team")]
    
    print(f"🔍 Found {len(personal_keys)} personal keys and {len(team_keys)} team keys")
    
    # Nếu có personal keys, ưu tiên chọn personal key
    if personal_keys:
        # Tìm personal key có tên phù hợp
        serverless_keywords = ["serverless", "model", "ai", "llm", "api", "test", "personal"]
        
        for key in personal_keys:
            key_name_lower = key["name"].lower()
            for keyword in serverless_keywords:
                if keyword in key_name_lower:
                    print(f"🎯 Found personal API key by keyword '{keyword}': {key['name']}")
                    return key
        
        # Nếu không tìm thấy theo keyword, chọn personal key đầu tiên
        print(f"🎯 Selected first personal key: {personal_keys[0]['name']}")
        return personal_keys[0]
    
    # Nếu không có personal keys, tìm team keys
    if team_keys:
        # Tìm team key có tên phù hợp
        serverless_keywords = ["serverless", "model", "ai", "llm", "api", "test"]
        
        for key in team_keys:
            key_name_lower = key["name"].lower()
            for keyword in serverless_keywords:
                if keyword in key_name_lower:
                    print(f"🎯 Found team API key by keyword '{keyword}': {key['name']}")
                    return key
        
        # Nếu không tìm thấy theo keyword, chọn team key đầu tiên
        print(f"🎯 Selected first team key: {team_keys[0]['name']}")
        return team_keys[0]
    
    # Cuối cùng, chọn key đầu tiên active
    print(f"🎯 Selected first active key: {active_keys[0]['name']}")
    return active_keys[0]

@pytest.fixture(scope="session")
def credits_api(config, auth_token):
    """Global CreditsAPI client for entire test session"""
    token, _, _ = auth_token  # Unpack tuple, ignore API key and all_keys
    return CreditsAPI(config["base_url"], api_key=token)

@pytest.fixture(scope="session")
def api_key_api(config, auth_token):
    """Global APIKeyAPI client for entire test session"""
    from api_clients.api_key import APIKeyAPI
    token, _, _ = auth_token  # Unpack tuple, ignore API key and all_keys
    return APIKeyAPI(config["base_url"], api_key=token)

@pytest.fixture(scope="session")
def personal_key(auth_token):
    """Get API key for serverless API tests"""
    _, api_key, _ = auth_token  # Unpack tuple, get API key, ignore all_keys
    if not api_key:
        print("⚠️ No API key available - using JWT token instead")
        # Fallback to JWT token if no API key
        token, _, _ = auth_token
        return token
    return api_key

@pytest.fixture(scope="session")
def all_api_keys(auth_token):
    """Get all available API keys for inspection"""
    _, _, all_keys = auth_token  # Unpack tuple, get all_keys
    if not all_keys:
        print("ℹ️ No API keys available - API key fetching was removed for performance")
    return all_keys

@pytest.fixture(scope="session")
def model_api(personal_key, serverless_base_url):
    """Global ModelAPI client for serverless API tests"""
    from api_clients.model_api import ModelAPI
    return ModelAPI(
        base_url=serverless_base_url,
        api_key=personal_key,
        timeout=30
    )

@pytest.fixture(scope="session")
def text_model_api(personal_key, serverless_base_url):
    """Global TextModelAPI client for text model tests (e.g., Mistral Small)"""
    from api_clients.text_model_api import TextModelAPI
    return TextModelAPI(
        base_model_url=serverless_base_url,
        api_key=personal_key
    )

@pytest.fixture(scope="session")
def serverless_base_url(config):
    """Get base URL for serverless API tests"""
    return config.get("model_base_url", config["base_url"])

def load_users_from_json():
    """Load user credentials from data/users.json"""
    try:
        with open("data/users.json", "r", encoding="utf-8") as file:
            users_data = json.load(file)
        return users_data
    except FileNotFoundError:
        raise FileNotFoundError("data/users.json not found. Please create this file with user credentials.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing data/users.json: {e}")

@pytest.fixture(scope="module")
def user_credentials():
    """Get all user credentials from data/users.json"""
    return load_users_from_json()

@pytest.fixture(scope="session")
def team_api(config, auth_token):
    """Global TeamAPI client for entire test session"""
    from api_clients.team_api import TeamAPI
    token, _, _ = auth_token  # Unpack tuple, ignore API key and all_keys
    return TeamAPI(config["base_url"], api_key=token)
