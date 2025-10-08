import pytest
import logging
import requests
import time
from datetime import datetime
from api_clients.text_models import TextModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_llm_statistics(base_url: str, auth_token: str, time_frame: str = "1d"):
    """
    Fetch LLM statistics from the API.
    
    Args:
        base_url: Base URL for the API
        auth_token: JWT token for authentication
        time_frame: Time frame for statistics (e.g., "1d", "7d")
        
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
    
    logger.debug(f"Statistics API response status: {response.status_code}")
    logger.debug(f"Statistics API response: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to get statistics: {response.status_code} - {response.text}")
        return None


def test_inference_usage_update_timing(config, auth_token, api_key_scope_session):
    """
    Test to determine how long it takes for the system to update inference usage statistics.
    
    This test:
    1. Gets initial usage statistics
    2. Makes a request to DeepSeek R1 Free model
    3. Polls the statistics API every 30 seconds to see when usage is updated
    4. Reports the time it takes for usage to be reflected in statistics
    """
    logger.info("🚀 Starting inference usage update timing test")
    logger.info("=" * 80)
    
    base_url = config["base_url"]
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics...")
        initial_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics"
        
        # Log the full response to understand its structure
        logger.info(f"   📋 Full API response: {initial_stats}")
        
        # Handle response structure - use top-level fields
        if isinstance(initial_stats, dict):
            if initial_stats.get("status") == "success":
                # Use top-level total fields from API response
                initial_total_requests = initial_stats.get("total_requests", 0)
                initial_total_tokens = initial_stats.get("total_tokens", 0)
            else:
                pytest.fail(f"Initial statistics request failed: {initial_stats}")
        else:
            pytest.fail(f"Unexpected response type: {type(initial_stats)}")
        
        logger.info(f"✅ Initial statistics retrieved:")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Step 2: Make a request to DeepSeek R1 Free
        logger.info("\n🤖 Step 2: Making request to DeepSeek R1 Free...")
        text_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
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
        logger.info("\n⏳ Step 3: Polling statistics API to detect usage update...")
        logger.info("   (Checking every 30 seconds, max 10 minutes)")
        
        max_attempts = 20  # 20 attempts * 30 seconds = 10 minutes max
        poll_interval = 30  # seconds
        usage_updated = False
        update_detected_at = None
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"\n   🔍 Attempt {attempt}/{max_attempts}...")
            time.sleep(poll_interval)
            
            current_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
            
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
                    
                    logger.info(f"\n🎉 Usage update detected!")
                    logger.info(f"   ✅ Request made at: {request_time.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Update detected at: {update_detected_at.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Time to update: {time_to_update:.0f} seconds ({time_to_update/60:.1f} minutes)")
                    logger.info(f"   ✅ Requests increased by: {current_total_requests - initial_total_requests}")
                    logger.info(f"   ✅ Tokens increased by: {current_total_tokens - initial_total_tokens}")
                    break
            else:
                logger.warning(f"      ⚠️  Failed to get statistics on attempt {attempt}")
        
        # Final result
        logger.info("\n" + "=" * 80)
        if usage_updated:
            time_to_update = (update_detected_at - request_time).total_seconds()
            logger.info(f"✅ TEST RESULT: Inference usage is updated within ~{time_to_update/60:.1f} minutes")
            logger.info(f"   (Exact time: {time_to_update:.0f} seconds)")
            
            # Assert that usage was updated (test passes)
            assert usage_updated, "Usage should be updated"
        else:
            logger.error(f"❌ TEST RESULT: Usage was NOT updated within {max_attempts * poll_interval / 60:.0f} minutes")
            logger.error("   This might indicate:")
            logger.error("   1. Statistics update delay is longer than expected")
            logger.error("   2. There might be an issue with the statistics tracking system")
            logger.error("   3. The API request might not have been counted")
            
            # This test will fail if usage is not updated within the time limit
            pytest.fail(f"Usage was not updated within {max_attempts * poll_interval / 60:.0f} minutes")
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        raise


def test_inference_usage_update_timing_7d(config, auth_token, api_key_scope_session):
    """
    Test to determine how long it takes for the system to update inference usage statistics.
    
    This test uses 7-day time frame to verify statistics tracking over a week.
    
    This test:
    1. Gets initial usage statistics (7d timeframe)
    2. Makes a request to DeepSeek R1 Free model
    3. Polls the statistics API every 30 seconds to see when usage is updated
    4. Reports the time it takes for usage to be reflected in statistics
    """
    logger.info("🚀 Starting inference usage update timing test (7-day timeframe)")
    logger.info("=" * 80)
    
    base_url = config["base_url"]
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics (7d timeframe)...")
        initial_stats = get_llm_statistics(base_url, auth_token, time_frame="7d")
        
        assert initial_stats is not None, "Failed to get initial statistics"
        
        # Handle response structure - use top-level fields
        if isinstance(initial_stats, dict):
            if initial_stats.get("status") == "success":
                # Use top-level total fields from API response
                initial_total_requests = initial_stats.get("total_requests", 0)
                initial_total_tokens = initial_stats.get("total_tokens", 0)
            else:
                pytest.fail(f"Initial statistics request failed: {initial_stats}")
        else:
            pytest.fail(f"Unexpected response type: {type(initial_stats)}")
        
        logger.info(f"✅ Initial statistics retrieved (7d):")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Step 2: Make a request to DeepSeek R1 Free
        logger.info("\n🤖 Step 2: Making request to DeepSeek R1 Free...")
        text_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
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
        logger.info("\n⏳ Step 3: Polling statistics API (7d) to detect usage update...")
        logger.info("   (Checking every 30 seconds, max 10 minutes)")
        
        max_attempts = 20  # 20 attempts * 30 seconds = 10 minutes max
        poll_interval = 30  # seconds
        usage_updated = False
        update_detected_at = None
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"\n   🔍 Attempt {attempt}/{max_attempts}...")
            time.sleep(poll_interval)
            
            current_stats = get_llm_statistics(base_url, auth_token, time_frame="7d")
            
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
                    
                    logger.info(f"\n🎉 Usage update detected in 7d statistics!")
                    logger.info(f"   ✅ Request made at: {request_time.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Update detected at: {update_detected_at.strftime('%H:%M:%S')}")
                    logger.info(f"   ✅ Time to update: {time_to_update:.0f} seconds ({time_to_update/60:.1f} minutes)")
                    logger.info(f"   ✅ Requests increased by: {current_total_requests - initial_total_requests}")
                    logger.info(f"   ✅ Tokens increased by: {current_total_tokens - initial_total_tokens}")
                    break
            else:
                logger.warning(f"      ⚠️  Failed to get statistics on attempt {attempt}")
        
        # Final result
        logger.info("\n" + "=" * 80)
        if usage_updated:
            time_to_update = (update_detected_at - request_time).total_seconds()
            logger.info(f"✅ TEST RESULT (7d): Inference usage is updated within ~{time_to_update/60:.1f} minutes")
            logger.info(f"   (Exact time: {time_to_update:.0f} seconds)")
            
            # Assert that usage was updated (test passes)
            assert usage_updated, "Usage should be updated"
        else:
            logger.error(f"❌ TEST RESULT (7d): Usage was NOT updated within {max_attempts * poll_interval / 60:.0f} minutes")
            logger.error("   This might indicate:")
            logger.error("   1. Statistics update delay is longer than expected")
            logger.error("   2. There might be an issue with the statistics tracking system")
            logger.error("   3. The API request might not have been counted")
            
            # This test will fail if usage is not updated within the time limit
            pytest.fail(f"Usage was not updated within {max_attempts * poll_interval / 60:.0f} minutes")
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        raise


def test_inference_usage_continuous_monitoring(config, auth_token, api_key_scope_session):
    """
    Test continuous monitoring of inference usage over 5 minutes.
    
    This test:
    1. Sends a request every 30 seconds
    2. Fetches statistics after each request
    3. Prints detailed results showing how statistics update
    4. Total duration: 5 minutes (10 requests total)
    """
    logger.info("🚀 Starting continuous inference usage monitoring test")
    logger.info("=" * 80)
    logger.info("📋 Test Plan:")
    logger.info("   - Duration: 5 minutes")
    logger.info("   - Fetch interval: 30 seconds")
    logger.info("   - Total requests to send: 10")
    logger.info("=" * 80)
    
    base_url = config["base_url"]
    num_requests = 10
    fetch_interval = 30  # seconds
    
    # Setup TextModelsAPI
    text_config = {
        "chat_completions_url": config["chat_completions_url"],
        "api_key": api_key_scope_session
    }
    text_api = TextModelsAPI(text_config)
    
    try:
        # Get initial statistics
        logger.info("\n📊 Getting initial statistics...")
        initial_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics"
        assert initial_stats.get("status") == "success", f"Initial statistics request failed: {initial_stats}"
        
        initial_total_requests = initial_stats.get("total_requests", 0)
        initial_total_tokens = initial_stats.get("total_tokens", 0)
        
        logger.info(f"✅ Initial statistics:")
        logger.info(f"   - Total requests: {initial_total_requests}")
        logger.info(f"   - Total tokens: {initial_total_tokens}")
        
        # Start monitoring
        logger.info("\n" + "=" * 80)
        logger.info("🔄 Starting continuous monitoring...")
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
            logger.info(f"\n   ⏳ Waiting {fetch_interval} seconds before fetching statistics...")
            time.sleep(fetch_interval)
            
            # Step 3: Fetch statistics
            logger.info(f"\n   📊 Fetching statistics...")
            fetch_time = datetime.now()
            current_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
            
            if current_stats and current_stats.get("status") == "success":
                current_total_requests = current_stats.get("total_requests", 0)
                current_total_tokens = current_stats.get("total_tokens", 0)
                
                requests_increase = current_total_requests - initial_total_requests
                tokens_increase = current_total_tokens - initial_total_tokens
                
                time_since_request = (fetch_time - request_time).total_seconds()
                
                logger.info(f"   ✅ Statistics fetched successfully!")
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
                logger.error(f"   ❌ Failed to fetch statistics")
        
        # Final summary
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 FINAL SUMMARY")
        logger.info("=" * 80)
        logger.info(f"⏱️  Total test duration: {total_duration:.0f} seconds ({total_duration/60:.1f} minutes)")
        logger.info(f"📨 Requests sent: {num_requests}")
        logger.info(f"📈 Requests tracked: {results[-1]['requests_increase'] if results else 0}")
        logger.info(f"🔢 Tokens tracked: {results[-1]['tokens_increase'] if results else 0}")
        
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
        logger.info(f"✅ Test completed successfully!")
        logger.info(f"   Expected to track: {num_requests} requests")
        logger.info(f"   Actually tracked: {results[-1]['requests_increase']} requests")
        
        # Assert that we tracked at least most of our requests
        # (allowing for a small delay in the last few)
        assert results[-1]['requests_increase'] >= num_requests - 2, \
            f"Expected at least {num_requests-2} requests to be tracked, but only {results[-1]['requests_increase']} were tracked"
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        raise


def test_inference_usage_multiple_requests(config, auth_token, api_key_scope_session):
    """
    Test to verify that multiple requests are correctly tracked in usage statistics.
    
    This test:
    1. Gets initial usage statistics
    2. Makes 3 requests to DeepSeek R1 Free model
    3. Waits for a reasonable time (3 minutes)
    4. Checks if all requests are reflected in statistics
    """
    logger.info("🚀 Starting inference usage multiple requests test")
    logger.info("=" * 80)
    
    base_url = config["base_url"]
    num_requests = 3
    
    try:
        # Step 1: Get initial statistics
        logger.info("\n📊 Step 1: Getting initial statistics...")
        initial_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
        
        assert initial_stats is not None, "Failed to get initial statistics"
        assert initial_stats.get("status") == "success", f"Initial statistics request failed: {initial_stats}"
        
        # Use top-level total fields from API response
        initial_total_requests = initial_stats.get("total_requests", 0)
        
        logger.info(f"✅ Initial total requests: {initial_total_requests}")
        
        # Step 2: Make multiple requests
        logger.info(f"\n🤖 Step 2: Making {num_requests} requests to DeepSeek R1 Free...")
        text_config = {
            "chat_completions_url": config["chat_completions_url"],
            "api_key": api_key_scope_session
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
        logger.info(f"\n⏳ Step 3: Waiting {wait_time} seconds for statistics to update...")
        time.sleep(wait_time)
        
        # Step 4: Check final statistics
        logger.info("\n📊 Step 4: Checking final statistics...")
        final_stats = get_llm_statistics(base_url, auth_token, time_frame="1d")
        
        assert final_stats is not None, "Failed to get final statistics"
        assert final_stats.get("status") == "success", f"Final statistics request failed: {final_stats}"
        
        # Use top-level total fields from API response
        final_total_requests = final_stats.get("total_requests", 0)
        
        requests_increase = final_total_requests - initial_total_requests
        
        logger.info(f"   - Initial requests: {initial_total_requests}")
        logger.info(f"   - Final requests: {final_total_requests}")
        logger.info(f"   - Increase: {requests_increase}")
        
        # Verify that the increase is at least the number of requests we made
        logger.info("\n" + "=" * 80)
        if requests_increase >= num_requests:
            logger.info(f"✅ TEST RESULT: All {num_requests} requests were tracked successfully!")
            logger.info(f"   Expected at least: {num_requests}")
            logger.info(f"   Actual increase: {requests_increase}")
        else:
            logger.warning(f"⚠️  TEST RESULT: Expected increase of at least {num_requests}, but got {requests_increase}")
            logger.warning(f"   This might indicate that statistics are still updating")
        
        logger.info("=" * 80)
        
        # Assert that at least our requests are counted
        assert requests_increase >= num_requests, \
            f"Expected at least {num_requests} new requests, but only {requests_increase} were tracked"
        
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        raise

