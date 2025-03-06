from serverless_api.base_test import NEBULA_API_KEY, TEXT_API_URL, test_results
import requests
import pytest
import logging


# test case
test_cases = [
    ("TC_00_CheckConnection", "Is this API working correctly?", 200),
    ("TC_01_ValidRequest", "Hello, how are you?", 200),
    ("TC_02_LongPrompt", "A" * 5000, 200),
    ("TC_03_SpecialCharacters", "What is 2+2? 😊", 200),
    ("TC_04_EmptyPrompt", "", 200),
    ("TC_05_InvalidAPIKey", "Hello", 401),
    ("TC_06_NoAPIKey", "Hello", 401),
]

@pytest.mark.parametrize("test_id, prompt, expected_status", test_cases)
def test_model_api(test_id, prompt, expected_status):
    """Test API với nhiều test case khác nhau"""
    headers = {"Content-Type": "application/json"}

    # Xử lý API key cho từng test case
    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False,
    }

    logging.info(f"Running {test_id}...")
    try:
        response = requests.post(TEXT_API_URL, headers=headers, json=data, timeout=10)
        response.raise_for_status()


        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"


        if response.status_code == 200:
            result = response.json()
            assert "choices" in result, f"Expected 'choices' in response, got: {result}"
            assert "message" in result["choices"][0], f"No message in response: {result['choices']}"
        elif response.status_code == 401:
            assert "error" in response.text.lower(), f"Expected error in response, got: {response.text}"

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        logging.error(f"{test_id} ❌ Failed! Error: {str(e)}")
        test_results.append((test_id, "❌ Failed", str(e)))
        pytest.fail(f"{test_id} failed: {str(e)}", pytrace=True)

