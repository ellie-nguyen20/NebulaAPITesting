import pytest
import logging
import requests
import time
import json
from pathlib import Path
from datetime import datetime
from api_clients.text_models import TextModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MegaNova API base URL
MEGANOVA_BASE_URL = "https://dev-portal-api.meganova.ai/api/v1"

@pytest.fixture(scope="session")
def meganova_auth_token(pytestconfig):
    """
    Get authentication token for MegaNova API.
    
    Returns:
        JWT token string for MegaNova API authentication
    """
    # Load user credentials
    users_file = Path(__file__).parent.parent.parent.parent / "data" / "users.json"
    with open(users_file, "r", encoding="utf-8") as f:
        users = json.load(f)
    
    # Get selected user
    user_name = pytestconfig.getoption("--user")
    if user_name and user_name in users:
        selected_user = users[user_name]
        logger.info(f"🔐 Logging into MegaNova as: {user_name} -> {selected_user['email']}")
    else:
        first_user_name = next(iter(users))
        selected_user = users[first_user_name]
        logger.info(f"🔐 Logging into MegaNova as default user: {first_user_name} -> {selected_user['email']}")
    
    # Login to MegaNova
    try:
        logger.info(f"🚀 Attempting MegaNova login with user: {selected_user['email']}")
        payload = {"username": selected_user["email"], "password": selected_user["password"]}
        resp = requests.post(f"{MEGANOVA_BASE_URL}/login", data=payload, timeout=10)
        
        logger.info(f"   MegaNova login response status: {resp.status_code}")
        
        if resp.status_code == 200:
            response_data = resp.json()
            logger.info(f"   MegaNova login response: {response_data}")
            
            if "data" in response_data and "jwtToken" in response_data["data"]:
                token = response_data["data"]["jwtToken"]
                logger.info("✅ MegaNova login successful - token will be reused for all tests")
                return token
            else:
                logger.error(f"❌ MegaNova login response missing jwtToken: {resp.text}")
        else:
            logger.error(f"❌ MegaNova login failed: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        logger.error(f"❌ MegaNova login error: {e}")
    
    raise Exception(f"Failed to login to MegaNova. Status: {resp.status_code}, Response: {resp.text}")


@pytest.fixture(scope="session")
def meganova_api_key(meganova_auth_token):
    """
    Get API key for MegaNova from the logged-in user.
    
    Returns:
        API key string for MegaNova serverless API calls
    """
    from api_clients.api_key import APIKeyAPI
    
    # Create API key client using MegaNova JWT token
    api_key_client = APIKeyAPI(MEGANOVA_BASE_URL, api_key=meganova_auth_token)
    
    try:
        # Get all API keys for the current user from MegaNova
        response = api_key_client.get_api_keys()
        
        if not response.ok:
            logger.error(f"Failed to get MegaNova API keys: {response.status_code} - {response.text}")
            raise Exception(f"Failed to get MegaNova API keys: {response.status_code}")
        
        api_keys_data = response.json()
        
        if api_keys_data.get("status") != "success":
            logger.error(f"MegaNova API keys response not successful: {api_keys_data}")
            raise Exception(f"MegaNova API keys response not successful: {api_keys_data.get('message', 'Unknown error')}")
        
        api_keys = api_keys_data.get("data", [])
        
        if not api_keys:
            logger.error("No API keys found for MegaNova")
            raise Exception("No API keys found for MegaNova")
        
        logger.info(f"Found {len(api_keys)} API keys for MegaNova")
        
        # Find personal key (team: null)
        personal_key = _find_personal_api_key_meganova(api_keys)
        
        if not personal_key:
            logger.error("No personal API key found for MegaNova (team: null). Test will be stopped.")
            raise Exception("No personal API key found for MegaNova (team: null). Test will be stopped.")
        
        logger.info(f"Found MegaNova personal API key: {personal_key['name'] or 'Unnamed'} (ID: {personal_key['id']})")
        
        return personal_key["key"]
        
    except Exception as e:
        logger.error(f"Error getting MegaNova personal API key: {e}")
        raise Exception(f"Failed to get MegaNova personal API key: {e}")


def _find_personal_api_key_meganova(api_keys):
    """
    Find personal API key from the MegaNova list (team: null).
    
    Args:
        api_keys: List of API key dictionaries from MegaNova
        
    Returns:
        Personal API key dictionary or None if not found
    """
    if not api_keys:
        return None
    
    # Filter active keys (status = 1)
    active_keys = [key for key in api_keys if key.get("status") == 1]
    
    if not active_keys:
        logger.warning("No active API keys found for MegaNova")
        return None
    
    # Find personal keys (team: null)
    personal_keys = [key for key in active_keys if key.get("team") is None]
    
    if not personal_keys:
        logger.error("No personal API keys found for MegaNova (team: null)")
        return None
    
    logger.info(f"Found {len(personal_keys)} personal API keys for MegaNova")
    
    # Return the first personal key found
    return personal_keys[0]


def get_llm_statistics_meganova(base_url: str, auth_token: str, time_frame: str = "1d"):
    """
    Fetch LLM statistics from the MegaNova API.
    
    Args:
        base_url: Base URL for the MegaNova API
        auth_token: JWT token for authentication
        time_frame: Time frame for statistics (supported: "1h", "1d")
        
    Returns:
        API response dictionary
    """
    url = f"{base_url}/serverless/llm-statistics"
    params = {"time_frame": time_frame}
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    logger.debug(f"MegaNova Statistics API response status: {response.status_code}")
    logger.debug(f"MegaNova Statistics API response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to get MegaNova statistics: {response.status_code} - {response.text}")
        return None


def test_inference_usage_update_timing_1d_meganova(config, meganova_auth_token, meganova_api_key):
    """
    Test to determine how long it takes for the MegaNova system to update inference usage statistics.
    
    This test uses 1-day time frame (7 days actual data) to verify statistics tracking.
    
    This test:
    1. Gets initial usage statistics (1d timeframe)
    2. Makes a request to DeepSeek R1 Free model
    3. Polls the statistics API every 30 seconds to see when usage is updated
    4. Reports the time it takes for usage to be reflected in statistics
    """
    logger.info("🚀 Starting MegaNova inference usage update timing test (1-day timeframe)")
    logger.info("=" * 80)
    
    # Use MegaNova API URL
    meganova_base_url = "https://dev-portal-api.meganova.ai/api/v1"
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics (1d timeframe) from MegaNova...")
        initial_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics from MegaNova"
        
        # Log the full response to understand its structure
        logger.info(f"   📋 Full MegaNova API response: {initial_stats}")
        
        # Handle response structure - use top-level fields
        if isinstance(initial_stats, dict):
            if initial_stats.get("status") == "success":
                # Use top-level total fields from API response
                initial_total_requests = initial_stats.get("total_requests", 0)
                initial_total_tokens = initial_stats.get("total_tokens", 0)
            else:
                pytest.fail(f"Initial MegaNova statistics request failed: {initial_stats}")
        else:
            pytest.fail(f"Unexpected response type from MegaNova: {type(initial_stats)}")
        
        logger.info(f"✅ Initial MegaNova statistics retrieved (1d):")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Step 2: Make a request to DeepSeek R1 Free
        logger.info("\n🤖 Step 2: Making request to DeepSeek R1 Free...")
        # Use MegaNova chat completions URL
        meganova_chat_url = "https://dev-llm-proxy.meganova.ai/v1/chat/completions"
        text_config = {
            "chat_completions_url": meganova_chat_url,
            "api_key": meganova_api_key
        }
        text_api = TextModelsAPI(text_config)
        
        request_time = datetime.now()
        logger.info(f"   ⏰ Request made at: {request_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        response = text_api.call_model(
            model_name="deepseek-r1-free",
            prompt="What is 2+2? Please answer in one sentence.",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, "Response should not be None"
        assert "choices" in response, f"Response should contain 'choices' field. Got: {response}"
        
        # Extract usage information from the response
        usage = response.get("usage", {})
        tokens_used = usage.get("total_tokens", 0)
        
        logger.info(f"✅ Model request successful!")
        logger.info(f"   - Tokens used in this request: {tokens_used}")
        logger.info(f"   - Response preview: {response['choices'][0]['message']['content'][:100]}...")
        
        # Step 3: Poll statistics API to see when usage updates
        logger.info("\n⏳ Step 3: Polling MegaNova statistics API (1d) to detect usage update...")
        logger.info("   (Checking every 30 seconds, max 10 minutes)")
        
        max_attempts = 20  # 20 attempts * 30 seconds = 10 minutes max
        poll_interval = 30  # seconds
        usage_updated = False
        update_detected_at = None
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"\n   🔍 Attempt {attempt}/{max_attempts}...")
            time.sleep(poll_interval)
            
            current_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
            
            if current_stats and current_stats.get("status") == "success":
                # Use top-level total fields from API response
                current_total_requests = current_stats.get("total_requests", 0)
                current_total_tokens = current_stats.get("total_tokens", 0)
                
                elapsed_time = (datetime.now() - request_time).total_seconds()
                
                logger.info(f"      - Time elapsed: {elapsed_time:.0f} seconds ({elapsed_time/60:.1f} minutes)")
                logger.info(f"      - Current total requests: {current_total_requests} (was {initial_total_requests})")
                logger.info(f"      - Current total tokens: {current_total_tokens} (was {initial_total_tokens})")
                
                # Check if usage has increased
                if current_total_requests > initial_total_requests or current_total_tokens > initial_total_tokens:
                    usage_updated = True
                    update_detected_at = datetime.now()
                    time_to_update = (update_detected_at - request_time).total_seconds()
                    
                    logger.info(f"\n🎉 Usage update detected in MegaNova 1d statistics!")
                    logger.info(f"   ✅ Request made at: {request_time.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Update detected at: {update_detected_at.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Time to update: {time_to_update:.0f} seconds ({time_to_update/60:.1f} minutes)")
                    logger.info(f"   ✅ Requests increased by: {current_total_requests - initial_total_requests}")
                    logger.info(f"   ✅ Tokens increased by: {current_total_tokens - initial_total_tokens}")
                    break
            else:
                logger.warning(f"      ⚠️  Failed to get MegaNova statistics on attempt {attempt}")
        
        # Final result
        logger.info("\n" + "=" * 80)
        if usage_updated:
            time_to_update = (update_detected_at - request_time).total_seconds()
            logger.info(f"✅ MEGANOVA TEST RESULT (1d): Inference usage is updated within ~{time_to_update/60:.1f} minutes")
            logger.info(f"   (Exact time: {time_to_update:.0f} seconds)")
            
            # Assert that usage was updated (test passes)
            assert usage_updated, "MegaNova usage should be updated"
        else:
            logger.error(f"❌ MEGANOVA TEST RESULT (1d): Usage was NOT updated within {max_attempts * poll_interval / 60:.0f} minutes")
            logger.error("   This might indicate:")
            logger.error("   1. MegaNova statistics update delay is longer than expected")
            logger.error("   2. There might be an issue with the MegaNova statistics tracking system")
            logger.error("   3. The API request might not have been counted by MegaNova")
            
            # This test will fail if usage is not updated within the time limit
            pytest.fail(f"MegaNova usage was not updated within {max_attempts * poll_interval / 60:.0f} minutes")
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ MegaNova test failed with error: {e}")
        raise


def test_inference_usage_update_timing_1h_meganova(config, meganova_auth_token, meganova_api_key):
    """
    Test to determine how long it takes for the MegaNova system to update inference usage statistics.
    
    This test uses 1-hour time frame to verify statistics tracking.
    
    This test:
    1. Gets initial usage statistics (1h timeframe)
    2. Makes a request to DeepSeek R1 Free model
    3. Polls the statistics API every 30 seconds to see when usage is updated
    4. Reports the time it takes for usage to be reflected in statistics
    """
    logger.info("🚀 Starting MegaNova inference usage update timing test (1-hour timeframe)")
    logger.info("=" * 80)
    
    # Use MegaNova API URL
    meganova_base_url = "https://dev-portal-api.meganova.ai/api/v1"
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics (1h timeframe) from MegaNova...")
        initial_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1h")
        
        assert initial_stats is not None, "Failed to get initial statistics from MegaNova"
        
        # Handle response structure - use top-level fields
        if isinstance(initial_stats, dict):
            if initial_stats.get("status") == "success":
                # Use top-level total fields from API response
                initial_total_requests = initial_stats.get("total_requests", 0)
                initial_total_tokens = initial_stats.get("total_tokens", 0)
            else:
                pytest.fail(f"Initial MegaNova statistics request failed: {initial_stats}")
        else:
            pytest.fail(f"Unexpected response type from MegaNova: {type(initial_stats)}")
        
        logger.info(f"✅ Initial MegaNova statistics retrieved (1h):")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Step 2: Make a request to DeepSeek R1 Free
        logger.info("\n🤖 Step 2: Making request to DeepSeek R1 Free...")
        # Use MegaNova chat completions URL
        meganova_chat_url = "https://dev-llm-proxy.meganova.ai/v1/chat/completions"
        text_config = {
            "chat_completions_url": meganova_chat_url,
            "api_key": meganova_api_key
        }
        text_api = TextModelsAPI(text_config)
        
        request_time = datetime.now()
        logger.info(f"   ⏰ Request made at: {request_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        response = text_api.call_model(
            model_name="deepseek-r1-free",
            prompt="What is 10+10? Please answer in one sentence.",
            system_message="You are a helpful assistant."
        )
        
        assert response is not None, "Response should not be None"
        assert "choices" in response, f"Response should contain 'choices' field. Got: {response}"
        
        # Extract usage information from the response
        usage = response.get("usage", {})
        tokens_used = usage.get("total_tokens", 0)
        
        logger.info(f"✅ Model request successful!")
        logger.info(f"   - Tokens used in this request: {tokens_used}")
        logger.info(f"   - Response preview: {response['choices'][0]['message']['content'][:100]}...")
        
        # Step 3: Poll statistics API to see when usage updates
        logger.info("\n⏳ Step 3: Polling MegaNova statistics API (1h) to detect usage update...")
        logger.info("   (Checking every 30 seconds, max 10 minutes)")
        
        max_attempts = 20  # 20 attempts * 30 seconds = 10 minutes max
        poll_interval = 30  # seconds
        usage_updated = False
        update_detected_at = None
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"\n   🔍 Attempt {attempt}/{max_attempts}...")
            time.sleep(poll_interval)
            
            current_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1h")
            
            if current_stats and current_stats.get("status") == "success":
                # Use top-level total fields from API response
                current_total_requests = current_stats.get("total_requests", 0)
                current_total_tokens = current_stats.get("total_tokens", 0)
                
                elapsed_time = (datetime.now() - request_time).total_seconds()
                
                logger.info(f"      - Time elapsed: {elapsed_time:.0f} seconds ({elapsed_time/60:.1f} minutes)")
                logger.info(f"      - Current total requests: {current_total_requests} (was {initial_total_requests})")
                logger.info(f"      - Current total tokens: {current_total_tokens} (was {initial_total_tokens})")
                
                # Check if usage has increased
                if current_total_requests > initial_total_requests or current_total_tokens > initial_total_tokens:
                    usage_updated = True
                    update_detected_at = datetime.now()
                    time_to_update = (update_detected_at - request_time).total_seconds()
                    
                    logger.info(f"\n🎉 Usage update detected in MegaNova 1h statistics!")
                    logger.info(f"   ✅ Request made at: {request_time.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Update detected at: {update_detected_at.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Time to update: {time_to_update:.0f} seconds ({time_to_update/60:.1f} minutes)")
                    logger.info(f"   ✅ Requests increased by: {current_total_requests - initial_total_requests}")
                    logger.info(f"   ✅ Tokens increased by: {current_total_tokens - initial_total_tokens}")
                    break
            else:
                logger.warning(f"      ⚠️  Failed to get MegaNova statistics on attempt {attempt}")
        
        # Final result
        logger.info("\n" + "=" * 80)
        if usage_updated:
            time_to_update = (update_detected_at - request_time).total_seconds()
            logger.info(f"✅ MEGANOVA TEST RESULT (1h): Inference usage is updated within ~{time_to_update/60:.1f} minutes")
            logger.info(f"   (Exact time: {time_to_update:.0f} seconds)")
            
            # Assert that usage was updated (test passes)
            assert usage_updated, "MegaNova usage should be updated"
        else:
            logger.error(f"❌ MEGANOVA TEST RESULT (1h): Usage was NOT updated within {max_attempts * poll_interval / 60:.0f} minutes")
            logger.error("   This might indicate:")
            logger.error("   1. MegaNova statistics update delay is longer than expected")
            logger.error("   2. There might be an issue with the MegaNova statistics tracking system")
            logger.error("   3. The API request might not have been counted by MegaNova")
            
            # This test will fail if usage is not updated within the time limit
            pytest.fail(f"MegaNova usage was not updated within {max_attempts * poll_interval / 60:.0f} minutes")
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ MegaNova test failed with error: {e}")
        raise


def test_inference_usage_continuous_monitoring_meganova(config, meganova_auth_token, meganova_api_key):
    """
    Test continuous monitoring of MegaNova inference usage over 5 minutes.
    
    This test:
    1. Sends a request every 30 seconds
    2. Fetches statistics after each request from MegaNova
    3. Prints detailed results showing how statistics update
    4. Total duration: 5 minutes (10 requests total)
    """
    logger.info("🚀 Starting MegaNova continuous inference usage monitoring test")
    logger.info("=" * 80)
    logger.info("📋 Test Plan:")
    logger.info("   - Duration: 5 minutes")
    logger.info("   - Fetch interval: 30 seconds")
    logger.info("   - Total requests to send: 10")
    logger.info("   - Target: MegaNova API")
    logger.info("=" * 80)
    
    # Use MegaNova API URL
    meganova_base_url = "https://dev-portal-api.meganova.ai/api/v1"
    num_requests = 10
    fetch_interval = 30  # seconds
    
    # Setup TextModelsAPI with MegaNova URL
    meganova_chat_url = "https://dev-llm-proxy.meganova.ai/v1/chat/completions"
    text_config = {
        "chat_completions_url": meganova_chat_url,
        "api_key": api_key_scope_session
    }
    text_api = TextModelsAPI(text_config)
    
    try:
        # Get initial statistics
        logger.info("\n📊 Getting initial statistics from MegaNova...")
        initial_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics from MegaNova"
        assert initial_stats.get("status") == "success", f"Initial MegaNova statistics request failed: {initial_stats}"
        
        initial_total_requests = initial_stats.get("total_requests", 0)
        initial_total_tokens = initial_stats.get("total_tokens", 0)
        
        logger.info(f"✅ Initial MegaNova statistics:")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Start monitoring
        logger.info("\n" + "=" * 80)
        logger.info("🔄 Starting MegaNova continuous monitoring...")
        logger.info("=" * 80)
        
        start_time = datetime.now()
        results = []
        
        prompts = [
            "What is 1+1?",
            "What is 2+2?",
            "What is 3+3?",
            "What is 4+4?",
            "What is 5+5?",
            "Name a planet.",
            "What color is the sky?",
            "What is water made of?",
            "How many days in a week?",
            "What comes after Monday?"
        ]
        
        for i in range(1, num_requests + 1):
            iteration_start = datetime.now()
            elapsed_total = (iteration_start - start_time).total_seconds()
            
            logger.info(f"\n{'='*80}")
            logger.info(f"📍 Iteration {i}/{num_requests} | Elapsed: {elapsed_total:.0f}s ({elapsed_total/60:.1f} min)")
            logger.info(f"{'='*80}")
            
            # Step 1: Send request
            logger.info(f"\n   🤖 Sending request {i}...")
            request_time = datetime.now()
            
            try:
                response = text_api.call_model(
                    model_name="deepseek-r1-free",
                    prompt=prompts[i-1],
                    system_message="You are a helpful assistant. Answer in one short sentence."
                )
                
                assert response is not None, f"Response {i} should not be None"
                assert "choices" in response, f"Response {i} should contain 'choices' field"
                
                usage = response.get("usage", {})
                tokens_used = usage.get("total_tokens", 0)
                content = response['choices'][0]['message']['content']
                
                logger.info(f"   ✅ Request {i} successful!")
                logger.info(f"      - Tokens used: {tokens_used}")
                logger.info(f"      - Response: {content[:80]}...")
                
            except Exception as e:
                logger.error(f"   ❌ Request {i} failed: {e}")
                tokens_used = 0
            
            # Step 2: Wait for fetch interval
            logger.info(f"\n   ⏳ Waiting {fetch_interval} seconds before fetching MegaNova statistics...")
            time.sleep(fetch_interval)
            
            # Step 3: Fetch statistics
            logger.info(f"\n   📊 Fetching MegaNova statistics...")
            fetch_time = datetime.now()
            current_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
            
            if current_stats and current_stats.get("status") == "success":
                current_total_requests = current_stats.get("total_requests", 0)
                current_total_tokens = current_stats.get("total_tokens", 0)
                
                requests_increase = current_total_requests - initial_total_requests
                tokens_increase = current_total_tokens - initial_total_tokens
                
                time_since_request = (fetch_time - request_time).total_seconds()
                
                logger.info(f"   ✅ MegaNova statistics fetched successfully!")
                logger.info(f"      - Time since request: {time_since_request:.0f}s")
                logger.info(f"      - Total requests: {current_total_requests} (+{requests_increase} from start)")
                logger.info(f"      - Total tokens: {current_total_tokens} (+{tokens_increase} from start)")
                
                # Store result
                results.append({
                    "iteration": i,
                    "request_time": request_time,
                    "fetch_time": fetch_time,
                    "time_since_request": time_since_request,
                    "tokens_used": tokens_used,
                    "total_requests": current_total_requests,
                    "total_tokens": current_total_tokens,
                    "requests_increase": requests_increase,
                    "tokens_increase": tokens_increase
                })
            else:
                logger.error(f"   ❌ Failed to fetch MegaNova statistics")
        
        # Final summary
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 MEGANOVA FINAL SUMMARY")
        logger.info("=" * 80)
        logger.info(f"⏱️  Total test duration: {total_duration:.0f} seconds ({total_duration/60:.1f} minutes)")
        logger.info(f"📨 Requests sent: {num_requests}")
        logger.info(f"📈 Requests tracked by MegaNova: {results[-1]['requests_increase'] if results else 0}")
        logger.info(f"🔢 Tokens tracked by MegaNova: {results[-1]['tokens_increase'] if results else 0}")
        
        logger.info("\n📋 Detailed Results:")
        logger.info(f"{'Iter':<6} {'Time Since Request':<20} {'Requests':<12} {'Tokens':<12} {'Status'}")
        logger.info("-" * 80)
        
        expected_tracked = 0
        for result in results:
            # Check if this request was tracked (increase from previous)
            if result['iteration'] == 1:
                prev_increase = 0
            else:
                prev_increase = results[result['iteration']-2]['requests_increase']
            
            current_increase = result['requests_increase']
            is_tracked = "✅ Tracked" if current_increase > prev_increase else "⏳ Pending"
            
            if current_increase > prev_increase:
                expected_tracked += 1
            
            logger.info(
                f"{result['iteration']:<6} "
                f"{result['time_since_request']:.0f}s{'':<17} "
                f"+{current_increase:<11} "
                f"+{result['tokens_increase']:<11} "
                f"{is_tracked}"
            )
        
        logger.info("=" * 80)
        logger.info(f"✅ MegaNova test completed successfully!")
        logger.info(f"   Expected to track: {num_requests} requests")
        logger.info(f"   Actually tracked: {results[-1]['requests_increase']} requests")
        
        # Assert that we tracked at least most of our requests
        # (allowing for a small delay in the last few)
        assert results[-1]['requests_increase'] >= num_requests - 2, \
            f"Expected at least {num_requests-2} requests to be tracked by MegaNova, but only {results[-1]['requests_increase']} were tracked"
        
    except Exception as e:
        logger.error(f"❌ MegaNova test failed with error: {e}")
        raise


def test_inference_usage_multiple_requests_meganova(config, meganova_auth_token, meganova_api_key):
    """
    Test to verify that multiple requests are correctly tracked in MegaNova usage statistics.
    
    This test:
    1. Gets initial usage statistics from MegaNova
    2. Makes 3 requests to DeepSeek R1 Free model
    3. Waits for a reasonable time (3 minutes)
    4. Checks if all requests are reflected in MegaNova statistics
    """
    logger.info("🚀 Starting MegaNova inference usage multiple requests test")
    logger.info("=" * 80)
    
    # Use MegaNova API URL
    meganova_base_url = "https://dev-portal-api.meganova.ai/api/v1"
    num_requests = 3
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics from MegaNova...")
        initial_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics from MegaNova"
        assert initial_stats.get("status") == "success", f"Initial MegaNova statistics request failed: {initial_stats}"
        
        # Use top-level total fields from API response
        initial_total_requests = initial_stats.get("total_requests", 0)
        
        logger.info(f"✅ Initial MegaNova total requests: {initial_total_requests}")
        
        # Step 2: Make multiple requests
        logger.info(f"\n🤖 Step 2: Making {num_requests} requests to DeepSeek R1 Free...")
        meganova_chat_url = "https://dev-llm-proxy.meganova.ai/v1/chat/completions"
        text_config = {
            "chat_completions_url": meganova_chat_url,
            "api_key": meganova_api_key
        }
        text_api = TextModelsAPI(text_config)
        
        prompts = [
            "What is 1+1?",
            "What is the capital of France?",
            "Name one planet in our solar system."
        ]
        
        first_request_time = datetime.now()
        
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"\n   Request {i}/{num_requests}: '{prompt}'")
            response = text_api.call_model(
                model_name="deepseek-r1-free",
                prompt=prompt,
                system_message="You are a helpful assistant. Answer in one sentence."
            )
            
            assert response is not None, f"Response {i} should not be None"
            assert "choices" in response, f"Response {i} should contain 'choices' field"
            
            content = response['choices'][0]['message']['content']
            logger.info(f"   ✅ Response {i}: {content[:100]}...")
            
            # Small delay between requests
            if i < num_requests:
                time.sleep(2)
        
        logger.info(f"\n✅ All {num_requests} requests completed!")
        
        # Step 3: Wait for statistics to update
        wait_time = 180  # 3 minutes
        logger.info(f"\n⏳ Step 3: Waiting {wait_time} seconds for MegaNova statistics to update...")
        time.sleep(wait_time)
        
        # Step 4: Check final statistics
        logger.info("\n📊 Step 4: Checking final MegaNova statistics...")
        final_stats = get_llm_statistics_meganova(meganova_base_url, meganova_auth_token, time_frame="1d")
        
        assert final_stats is not None, "Failed to get final statistics from MegaNova"
        assert final_stats.get("status") == "success", f"Final MegaNova statistics request failed: {final_stats}"
        
        # Use top-level total fields from API response
        final_total_requests = final_stats.get("total_requests", 0)
        
        requests_increase = final_total_requests - initial_total_requests
        
        logger.info(f"   - Initial requests: {initial_total_requests}")
        logger.info(f"   - Final requests: {final_total_requests}")
        logger.info(f"   - Increase: {requests_increase}")
        
        # Verify that the increase is at least the number of requests we made
        logger.info("\n" + "=" * 80)
        if requests_increase >= num_requests:
            logger.info(f"✅ MEGANOVA TEST RESULT: All {num_requests} requests were tracked successfully!")
            logger.info(f"   Expected at least: {num_requests}")
            logger.info(f"   Actual increase: {requests_increase}")
        else:
            logger.warning(f"⚠️  MEGANOVA TEST RESULT: Expected increase of at least {num_requests}, but got {requests_increase}")
            logger.warning(f"   This might indicate that MegaNova statistics are still updating")
        
        logger.info("=" * 80)
        
        # Assert that at least our requests are counted
        assert requests_increase >= num_requests, \
            f"Expected at least {num_requests} new requests to be tracked by MegaNova, but only {requests_increase} were tracked"
        
    except Exception as e:
        logger.error(f"❌ MegaNova test failed with error: {e}")
        raise
