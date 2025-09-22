import pytest
import yaml
import json
import requests
import logging
from pathlib import Path
from api_clients.credit_api import CreditsAPI
from api_clients.ssh_key import SSHKeyAPI
from api_clients.embedding_api import EmbeddingAPI
from api_clients.rerank_api import RerankAPI
from api_clients.vision_api import VisionAPI
from api_clients.image_api import ImageAPI
from api_clients.video_api import VideoAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to users.json
USERS_FILE = Path(__file__).parent / "data" / "users.json"

# Load all users at pytest startup
with open(USERS_FILE, "r", encoding="utf-8") as f:
    USERS = json.load(f)

def load_config() -> dict:
    """
    Load configuration from config.yaml file.
    Direct configuration without environment separation.
    
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config.yaml not found
        ValueError: If YAML parsing error
    """
    try:
        with open("config.yaml", "r") as file:
            config_data = yaml.safe_load(file)
        
        # Validate required fields
        required_fields = ["base_url", "model_base_url"]
        for field in required_fields:
            if field not in config_data:
                raise ValueError(f"Required field '{field}' not found in config.yaml")
        
        # Add full endpoint URLs if not present
        if "chat_completions_url" not in config_data:
            config_data["chat_completions_url"] = f"{config_data['model_base_url']}/v1/chat/completions"
        if "image_generation_url" not in config_data:
            config_data["image_generation_url"] = f"{config_data['base_url']}/api/v1/images/generation"
        if "embedding_url" not in config_data:
            config_data["embedding_url"] = f"{config_data['model_base_url']}/v1/embeddings"
        
        logger.info("✅ Loaded configuration from config.yaml")
        return config_data
        
    except FileNotFoundError:
        raise FileNotFoundError("config.yaml not found. Please create this file.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing config.yaml: {e}")

def pytest_addoption(parser) -> None:
    """
    Add custom command line options for pytest.
    
    Args:
        parser: Pytest argument parser
    """
    parser.addoption(
        "--user",
        action="store",
        default=None,
        help="User name from users.json to use (e.g., Ellie, Member1, Member4)"
    )

@pytest.fixture(scope="session")
def config() -> dict:
    """
    Load configuration for the test session.
    
    Returns:
        Configuration dictionary with environment settings (without API key)
    """
    return load_config()

@pytest.fixture(scope="session")
def config_with_api_key(config, api_key_scope_session) -> dict:
    """
    Configuration with API key from logged-in user.
    
    Returns:
        Configuration dictionary with API key from login
    """
    config_with_key = config.copy()
    config_with_key["api_key"] = api_key_scope_session
    logger.info("✅ Using API key from logged-in user")
    return config_with_key

@pytest.fixture(scope="session")
def selected_user(pytestconfig) -> dict:
    """
    Returns the selected user info based on CLI option or defaults to the first user.
    
    Returns:
        Dictionary containing user credentials (email, password)
    """
    user_name = pytestconfig.getoption("--user")

    if user_name:
        if user_name in USERS:
            chosen = USERS[user_name]
            logger.info(f"[pytest] Using user from CLI: {user_name} -> {chosen['email']}")
            return chosen
        else:
            pytest.exit(f"[pytest] ❌ User '{user_name}' not found in {USERS_FILE}")

    # Fallback to the first user in the JSON
    first_user_name = next(iter(USERS))
    chosen = USERS[first_user_name]
    logger.info(f"[pytest] No --user provided, using default: {first_user_name} -> {chosen['email']}")
    return chosen

@pytest.fixture(scope="session")
def auth_token(config, selected_user) -> str:
    """
    Get authentication token once for entire test session.
    
    Returns:
        JWT token string for API authentication
        
    Raises:
        Exception: If login fails
    """
    base_url = config["base_url"]
    
    try:
        logger.info(f"Login once for entire test session with user: {selected_user['email']}")
        payload = {"username": selected_user["email"], "password": selected_user["password"]}
        resp = requests.post(f"{base_url}/login", data=payload, timeout=10)
        
        if resp.status_code == 200:
            response_data = resp.json()
            if "data" in response_data and "jwtToken" in response_data["data"]:
                token = response_data["data"]["jwtToken"]
                logger.info("✅ Login successful - token will be reused for all tests")
                
                # Trả về chỉ token
                return token
            else:
                logger.error(f"Login response missing jwtToken: {resp.text}")
        else:
            logger.error(f"Login failed: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        logger.error(f"Login error: {e}")
    
    raise Exception(f"Failed to login. Status: {resp.status_code}, Response: {resp.text}")

@pytest.fixture(scope="session")
def api_key_scope_session(config, auth_token):
    """
    Get personal API key for the currently logged-in user.
    
    This fixture fetches the user's API keys using their JWT token
    and returns ONLY the personal key (team: null).
    
    Returns:
        Personal API key string for serverless API calls
        
    Raises:
        Exception: If no personal API key found (team: null)
    """
    from api_clients.api_key import APIKeyAPI
    
    # Create API key client using JWT token
    api_key_client = APIKeyAPI(config["base_url"], api_key=auth_token)
    
    try:
        # Get all API keys for the current user
        response = api_key_client.get_api_keys()
        
        if not response.ok:
            logger.error(f"Failed to get API keys: {response.status_code} - {response.text}")
            raise Exception(f"Failed to get API keys: {response.status_code}")
        
        api_keys_data = response.json()
        
        if api_keys_data.get("status") != "success":
            logger.error(f"API keys response not successful: {api_keys_data}")
            raise Exception(f"API keys response not successful: {api_keys_data.get('message', 'Unknown error')}")
        
        api_keys = api_keys_data.get("data", [])
        
        if not api_keys:
            logger.error("No API keys found for team")
            raise Exception("No API keys found for team")
        
        logger.info(f"Found {len(api_keys)} API keys for team")
        
        # Find personal key (team: null)
        personal_key = _find_personal_api_key(api_keys)
        
        if not personal_key:
            logger.error("No personal API key found (team: null). Test will be stopped.")
            raise Exception("No personal API key found (team: null). Test will be stopped.")
        
        logger.info(f"Found personal API key: {personal_key['name'] or 'Unnamed'} (ID: {personal_key['id']})")
        
        return personal_key["key"]
        
    except Exception as e:
        logger.error(f"Error getting personal API key: {e}")
        raise Exception(f"Failed to get personal API key: {e}")

def _find_personal_api_key(api_keys):
    """
    Find personal API key from the list (team: null).
    
    Args:
        api_keys: List of API key dictionaries
        
    Returns:
        Personal API key dictionary or None if not found
    """
    if not api_keys:
        return None
    
    # Filter active keys (status = 1)
    active_keys = [key for key in api_keys if key.get("status") == 1]
    
    if not active_keys:
        logger.warning("No active API keys found")
        return None
    
    # Find personal keys (team: null)
    personal_keys = [key for key in active_keys if key.get("team") is None]
    
    if not personal_keys:
        logger.error("No personal API keys found (team: null)")
        return None
    
    logger.info(f"Found {len(personal_keys)} personal API keys")
    
    # Return the first personal key found
    return personal_keys[0]

@pytest.fixture(scope="session")
def credits_api(config, auth_token) -> CreditsAPI:
    """
    Global CreditsAPI client for entire test session.
    
    Returns:
        CreditsAPI client instance
    """
    return CreditsAPI(config["base_url"], api_key=auth_token)

@pytest.fixture(scope="session")
def model_api(api_key_scope_session, serverless_base_url):
    """
    Global ModelAPI client for serverless API tests.
    
    Returns:
        ModelAPI client instance
    """
    from api_clients.model_api import ModelAPI
    return ModelAPI(
        base_url=serverless_base_url,
        api_key=api_key_scope_session,
        timeout=30
    )

@pytest.fixture(scope="session")
def text_model_api(api_key_scope_session, serverless_base_url):
    """
    Global TextModelAPI client for text model tests (e.g., Mistral Small).
    
    Returns:
        TextModelAPI client instance
    """
    from api_clients.text_model_api import TextModelAPI
    return TextModelAPI(
        base_model_url=serverless_base_url,
        api_key=api_key_scope_session
    )

@pytest.fixture(scope="session")
def serverless_base_url(config) -> str:
    """
    Get base URL for serverless API tests.
    
    Returns:
        Base URL string for serverless API endpoints
    """
    return config.get("model_base_url", config["base_url"])

def load_users_from_json() -> dict:
    """
    Load user credentials from data/users.json file.
    
    Returns:
        Dictionary containing user credentials
        
    Raises:
        FileNotFoundError: If users.json not found
        ValueError: If JSON parsing error
    """
    try:
        with open("data/users.json", "r", encoding="utf-8") as file:
            users_data = json.load(file)
        
        # Validate users structure
        for user_name, user_data in users_data.items():
            required_fields = ["email", "password"]
            for field in required_fields:
                if field not in user_data:
                    logger.warning(f"User '{user_name}' missing required field: {field}")
        
        return users_data
    except FileNotFoundError:
        raise FileNotFoundError("data/users.json not found. Please create this file with user credentials.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing data/users.json: {e}")

@pytest.fixture(scope="module")
def user_credentials() -> dict:
    """
    Get all user credentials from data/users.json.
    
    Returns:
        Dictionary containing all user credentials
    """
    return load_users_from_json()

@pytest.fixture(scope="session")
def team_api(config, auth_token):
    """
    Global TeamAPI client for entire test session.
    
    Returns:
        TeamAPI client instance
    """
    from api_clients.team_api import TeamAPI
    return TeamAPI(config["base_url"], api_key=auth_token)

@pytest.fixture(scope="session")
def api_key_api(config, auth_token):
    """
    Global APIKeyAPI client for entire test session.
    
    Returns:
        APIKeyAPI client instance
    """
    from api_clients.api_key import APIKeyAPI
    return APIKeyAPI(config["base_url"], api_key=auth_token)

@pytest.fixture(scope="session")
def ssh_key_api(config, auth_token):
    """
    Global SSHKeyAPI client for entire test session.
    
    Returns:
        SSHKeyAPI client instance
    """
    return SSHKeyAPI(config["base_url"], api_key=auth_token)

@pytest.fixture(scope="module")
def api_key_scope_module(config, auth_token):
    """
    Get personal API key for the currently logged-in user.
    
    This fixture fetches the user's API keys using their JWT token
    and returns ONLY the personal key (team: null).
    
    Scope: module - API key is fetched once per test module
    
    Returns:
        Personal API key string for serverless API calls
        
    Raises:
        Exception: If no personal API key found (team: null)
    """
    from api_clients.api_key import APIKeyAPI
    
    # Create API key client using JWT token
    api_key_client = APIKeyAPI(config["base_url"], api_key=auth_token)
    
    try:
        # Get all API keys for the current user
        response = api_key_client.get_api_keys()
        
        if not response.ok:
            logger.error(f"Failed to get API keys: {response.status_code} - {response.text}")
            raise Exception(f"Failed to get API keys: {response.status_code}")
        
        api_keys_data = response.json()
        
        if api_keys_data.get("status") != "success":
            logger.error(f"API keys response not successful: {api_keys_data}")
            raise Exception(f"API keys response not successful: {api_keys_data.get('message', 'Unknown error')}")
        
        api_keys = api_keys_data.get("data", [])
        
        if not api_keys:
            logger.error("No API keys found for user")
            raise Exception("No API keys found for user")
        
        logger.info(f"Found {len(api_keys)} API keys for user")
        
        # Find personal key (team: null)
        personal_key = _find_personal_api_key(api_keys)
        
        if not personal_key:
            logger.error("No personal API key found (team: null). Test will be stopped.")
            raise Exception("No personal API key found (team: null). Test will be stopped.")
        
        logger.info(f"Found personal API key: {personal_key['name'] or 'Unnamed'} (ID: {personal_key['id']})")
        
        return personal_key["key"]
        
    except Exception as e:
        logger.error(f"Error getting personal API key: {e}")
        raise Exception(f"Failed to get personal API key: {e}")

@pytest.fixture
def login_as_user(config):
    """
    Login as a specific user and return their config with API key.
    
    This fixture allows individual test cases to select which user to login as.
    Usage: user_config = login_as_user("Member9")
    
    Args:
        config: Base configuration from conftest.py
        
    Returns:
        Function that takes user_id and returns user config with API key
    """
    def _login_as_user(user_id: str) -> dict:
        """
        Login as specific user and return their config.
        
        Args:
            user_id: User ID from data/users.json (e.g., "Member9", "Ellie")
            
        Returns:
            User configuration dictionary with API key
        """
        from utils.auth import login_user
        
        logger.info(f"🔐 Logging in as user: {user_id}")
        
        try:
            # Login user and get JWT token
            auth_token = login_user(user_id)
            logger.info(f"✅ Successfully logged in as {user_id}")
            
            # Get API key for this user
            from api_clients.api_key import APIKeyAPI
            api_key_client = APIKeyAPI(config["base_url"], api_key=auth_token)
            
            # Get all API keys for the current user
            response = api_key_client.get_api_keys()
            
            if not response.ok:
                logger.error(f"Failed to get API keys: {response.status_code} - {response.text}")
                raise Exception(f"Failed to get API keys: {response.status_code}")
            
            api_keys_data = response.json()
            
            if api_keys_data.get("status") != "success":
                logger.error(f"API keys response not successful: {api_keys_data}")
                raise Exception(f"API keys response not successful: {api_keys_data.get('message', 'Unknown error')}")
            
            api_keys = api_keys_data.get("data", [])
            
            if not api_keys:
                logger.error("No API keys found for team")
                raise Exception("No API keys found for team")
            
            logger.info(f"Found {len(api_keys)} API keys for team")
            
            # Find personal key (team: null)
            personal_key = _find_personal_api_key(api_keys)
            
            if not personal_key:
                logger.error("No personal API key found (team: null). Test will be stopped.")
                raise Exception("No personal API key found (team: null). Test will be stopped.")
            
            logger.info(f"Found personal API key: {personal_key['name'] or 'Unnamed'} (ID: {personal_key['id']})")
            
            # Combine base config with user's API key
            user_config = config.copy()
            user_config["api_key"] = personal_key["key"]
            
            return user_config
            
        except Exception as e:
            logger.error(f"❌ Failed to login as {user_id}: {e}")
            raise Exception(f"Failed to login as {user_id}: {e}")
    
    return _login_as_user

@pytest.fixture(scope="session")
def embedding_api(config, api_key_scope_session):
    """
    Global EmbeddingAPI client for entire test session.
    
    Returns:
        EmbeddingAPI client instance
    """
    embedding_config = {
        "embedding_url": config["embedding_url"],
        "api_key": api_key_scope_session
    }
    return EmbeddingAPI(embedding_config)

@pytest.fixture(scope="session")
def rerank_api(config, api_key_scope_session):
    """
    Global RerankAPI client for entire test session.
    
    Returns:
        RerankAPI client instance
    """
    rerank_config = {
        "rerank_url": config["rerank_url"],
        "api_key": api_key_scope_session
    }
    return RerankAPI(rerank_config)

@pytest.fixture(scope="session")
def vision_api(config, api_key_scope_session):
    """
    Global VisionAPI client for entire test session.
    
    Returns:
        VisionAPI client instance
    """
    vision_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    return VisionAPI(vision_config)

@pytest.fixture(scope="session")
def image_api(config, api_key_scope_session):
    """
    Global ImageAPI client for entire test session.
    
    Returns:
        ImageAPI client instance
    """
    image_config = {
        "image_generation_url": config["image_generation_url"],
        "api_key": api_key_scope_session
    }
    return ImageAPI(image_config)

@pytest.fixture(scope="session")
def video_api(config, api_key_scope_session):
    """
    Global VideoAPI client for entire test session.
    
    Returns:
        VideoAPI client instance
    """
    video_config = {
        "video_generation_url": config["video_generation_url"],
        "api_key": api_key_scope_session
    }
    return VideoAPI(video_config)