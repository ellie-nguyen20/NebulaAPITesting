import pytest
import aiohttp
import asyncio
import logging
import time
import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Independent configuration for this file
def load_independent_config():
    """Load configuration independently for this test file"""
    # Default staging configuration
    config = {
        "base_url": "https://dev-llm-proxy.nebulablock.com/v1/chat/completions",
    }
    
    
    # Load API keys from environment variables for each tier
    for tier_config in tier_configs:
        env_var = tier_config["env_var"]
        api_key = os.getenv(env_var)
        if api_key:
            config[env_var] = api_key
            logger.info(f"Loaded API key for {tier_config['tier']} from {env_var}")
        else:
            logger.warning(f"API key not found for {tier_config['tier']} in environment variable: {env_var}")
    
    return config

# Test cases for different tiers based on the image
tier_configs = [
    {
        "tier": "Engineer Tier 1",
        "requirement": "Sign Up",
        "gpu": False,
        "cpu": False,
        "rpd": 200,
        "env_var": "ENGINEER_TIER_1"  # API key for this tier
    },
    {
        "tier": "Engineer Tier 2", 
        "requirement": "Add Credit Card",
        "gpu": False,
        "cpu": True,
        "rpd": 1000,
        "env_var": "ENGINEER_TIER_2"
    },
    {
        "tier": "Engineer Tier 3",
        "requirement": "Deposit $10", 
        "gpu": True,
        "cpu": True,
        "rpd": 2000,
        "env_var": "ENGINEER_TIER_3"
    },
    {
        "tier": "Expert Tier 1",
        "requirement": "Spend $30",
        "gpu": True,
        "cpu": True,
        "rpd": "unlimited",
        "env_var": "EXPERT_TIER_1"
    },
    {
        "tier": "Expert Tier 2",
        "requirement": "Spend $50",
        "gpu": True,
        "cpu": True,
        "rpd": "unlimited",
        "env_var": "EXPERT_TIER_2"
    }
]

def get_api_key_for_tier(tier_config, config):
    """Get API key for specific tier from config"""
    env_var = tier_config["env_var"]
    api_key = config.get(env_var)
    if not api_key:
        pytest.skip(f"API key for {tier_config['tier']} not found in config: {env_var}")
    return api_key

# Pytest fixture for independent config
@pytest.fixture(scope="module")
def independent_config():
    """Independent configuration fixture for this test file"""
    return load_independent_config()

# Pytest fixture for backward compatibility
@pytest.fixture(scope="module")
def config(independent_config):
    """Backward compatibility fixture that returns the independent config"""
    return independent_config

async def make_request_async(session, api_key, base_url, request_number):
    """Make a single API request using aiohttp"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "messages": [{"role": "user", "content": f"Test request #{request_number}. Hi"}],
        "model":"deepseek-ai/DeepSeek-V3-0324-Free",
        "max_tokens": 50,
        "temperature": 0.7,
        "stream": False,
    }
    
    try:
        async with session.post(base_url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                response_data = await response.json()
                return response.status, response_data
            else:
                response_text = await response.text()
                return response.status, response_text
    except Exception as e:
        return None, str(e)

def validate_response(response_data):
    """Validate the response structure"""
    assert "choices" in response_data, "Response missing 'choices' field"
    assert isinstance(response_data["choices"], list), "'choices' is not a list"
    assert len(response_data["choices"]) > 0, "'choices' is empty"
    assert "message" in response_data["choices"][0], "Missing 'message' in first choice"

async def run_concurrent_requests(api_key, base_url, num_requests, max_concurrent=10, time_delay=0.1):
    """Run multiple requests concurrently with rate limiting"""
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        successful_requests = 0
        rate_limited_requests = 0
        failed_requests = 0
        rate_limited_at = None
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def make_request_with_semaphore(request_num):
            async with semaphore:
                status_code, response_data = await make_request_async(session, api_key, base_url, request_num)
                await asyncio.sleep(time_delay)  # Small delay between requests
                return request_num, status_code, response_data
        
        # Create tasks for all requests
        tasks = [make_request_with_semaphore(i) for i in range(1, num_requests + 1)]
        
        # Execute all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                failed_requests += 1
                logging.error(f"Request failed with exception: {result}")
                continue
                
            request_num, status_code, response_data = result
            
            if status_code == 200:
                successful_requests += 1
                validate_response(response_data)
            elif status_code == 429:
                rate_limited_requests += 1
                if rate_limited_at is None:
                    rate_limited_at = request_num
                logging.info(f"Request {request_num}: RATE LIMITED (429)")
            else:
                failed_requests += 1
                logging.error(f"Request {request_num}: FAILED ({status_code}) - {response_data}")
        
        return successful_requests, rate_limited_requests, failed_requests, rate_limited_at

# Test Case 01 Engineer Tier 1 - Test up to 200 requests
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
async def test_tc01_tier1_200_requests(independent_config):
    """TC: Tier 1 should allow 199 requests, then allow 200th, and block 201st"""
    tier_config = tier_configs[0]  # Tier 1
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging - using both logger and print
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")

    # Step 1: Send 199 requests first
    success_199, rate_limit_199, fail_199, _ = await run_concurrent_requests(
        api_key, independent_config['base_url'], 199
    )
    assert success_199 == 199, f"Expected 199 successful requests, got {success_199}"
    assert rate_limit_199 == 0, f"Expected 0 rate-limited requests, got {rate_limit_199}"
    assert fail_199 == 0, f"Expected 0 failed requests, got {fail_199}"

    # Step 2: Send 200th request – still succeeds
    success_1, rate_limit_1, fail_1, _ = await run_concurrent_requests(
        api_key, independent_config['base_url'], 1
    )
    assert success_1 == 1, "The 200th request should succeed"
    
    # Step 3: Send 201st request – will be rate limited
    success_2, rate_limit_2, fail_2, _ = await run_concurrent_requests(
        api_key, independent_config['base_url'], 1
    )
    assert rate_limit_2 == 1, "The 201st request should be rate limited"

    """TC03: Engineer Tier 1 should reject 201st request with 429"""
    tier_config = tier_configs[0]  # Engineer Tier 1
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2
    )
    
    assert successful_requests == 200, f"Should complete 200 requests, got {successful_requests}"
    assert rate_limited_requests >= 1, f"Should have at least 1 rate limited request, got {rate_limited_requests}"
    assert rate_limited_at == 201, f"Should be rate limited at request 201, got {rate_limited_at}"

# Test Case 02: Engineer Tier 2 - Test up to 1000 requests
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
async def test_tc02_tier2_1000_requests(independent_config):
    """TC02: Engineer Tier 2 should handle up to 1000 requests"""
    tier_config = tier_configs[1]  # Engineer Tier 2
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2
    )
    
    assert successful_requests >= 1000, f"Should handle at least 1000 requests, got {successful_requests}"
    if rate_limited_at:
        assert rate_limited_at > 1000, f"Should not be rate limited before 1000 requests, got rate limited at {rate_limited_at}"

# Test Case 03: Engineer Tier 3 - Test up to 2000 requests
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
async def test_tc03_tier3_2000_requests(independent_config):
    """TC03: Engineer Tier 3 should handle up to 2000 requests"""
    tier_config = tier_configs[2]  # Engineer Tier 3
    api_key = get_api_key_for_tier(tier_config, independent_config) 
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2 , max_concurrent=100, time_delay=1.0
    )
    
    assert successful_requests >= 2000, f"Should handle at least 2000 requests, got {successful_requests}"
    if rate_limited_at:
        assert rate_limited_at > 2000, f"Should not be rate limited before 2000 requests, got rate limited at {rate_limited_at}"

# Test Case 04: Expert Tier 1 - Test unlimited requests (3000 requests)
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
async def test_tc04_expert1_3000_requests(independent_config):
    """TC04: Expert Tier 1 should handle 3000 requests (unlimited tier)"""
    tier_config = tier_configs[3]  # Expert Tier 1
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2, max_concurrent=100, time_delay=1.0
    )
    
    assert successful_requests == 3000, f"Should complete 3000 requests, got {successful_requests}"
    assert rate_limited_requests == 0, f"Should not have rate limited requests, got {rate_limited_requests}"
    assert failed_requests == 0, f"Should not have failed requests, got {failed_requests}"

    """TC07: Expert Tier 1 should handle 3000 requests (unlimited tier)"""
    tier_config = tier_configs[3]  # Expert Tier 1
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2
    )
    
    assert successful_requests == 3000, f"Should complete 3000 requests, got {successful_requests}"
    assert rate_limited_requests == 0, f"Should not have rate limited requests, got {rate_limited_requests}"
    assert failed_requests == 0, f"Should not have failed requests, got {failed_requests}"

# Test Case 05: Expert Tier 2 - Test unlimited requests (3500 requests)
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
async def test_tc05_expert2_3500_requests(independent_config):
    """TC05: Expert Tier 2 should handle 3500 requests (unlimited tier)"""
    tier_config = tier_configs[4]  # Expert Tier 2
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 2, max_concurrent=200, time_delay=1.0
    )
    
    assert successful_requests == 3500, f"Should complete 3500 requests, got {successful_requests}"
    assert rate_limited_requests == 0, f"Should not have rate limited requests, got {rate_limited_requests}"
    assert failed_requests == 0, f"Should not have failed requests, got {failed_requests}"

# Test Case 06: RPD Reset Test (requires manual execution after 24h)
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
@pytest.mark.skip(reason="This test requires manual execution after 24h or system reset")
async def test_tc06_rpd_reset(independent_config):
    """TC06: Test RPD reset after 24h - should allow requests again"""
    tier_config = tier_configs[0]  # Engineer Tier 1
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    # This test should be run manually after 24h or system reset
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 1
    )
    
    assert successful_requests == 1, f"After reset, first request should succeed, got {successful_requests}"
    assert rate_limited_requests == 0, f"Should not have rate limited requests after reset"

# Test Case 07: Test that each tier has the correct capabilities (GPU/CPU access)
# @pytest.mark.skip(reason="Skipping individual test cases")
@pytest.mark.asyncio
@pytest.mark.parametrize("tier_config", tier_configs)
async def test_tc07_tier_capabilities(tier_config, independent_config):
    """Test that each tier has the correct capabilities (GPU/CPU access)"""
    tier_name = tier_config["tier"]
    
    # Get API key for this tier
    api_key = get_api_key_for_tier(tier_config, independent_config)
    
    # Log API key for debugging
    log_message = f"Using API key for {tier_config['tier']}: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}"
    logger.info(log_message)
    print(f"DEBUG: {log_message}")
    
    # Test basic functionality with DeepSeek R1
    successful_requests, rate_limited_requests, failed_requests, rate_limited_at = await run_concurrent_requests(
        api_key, independent_config['base_url'], 1
    )
    
    assert successful_requests == 1, f"{tier_name}: Basic API call should succeed"
    assert rate_limited_requests == 0, f"{tier_name}: Should not be rate limited for single request"
    assert failed_requests == 0, f"{tier_name}: Should not have failed requests"
    
    logging.info(f"{tier_name}: Basic functionality test PASSED")
    logging.info(f"  GPU Access: {tier_config['gpu']}")
    logging.info(f"  CPU Access: {tier_config['cpu']}")
    logging.info(f"  RPD Limit: {tier_config['rpd']}")
