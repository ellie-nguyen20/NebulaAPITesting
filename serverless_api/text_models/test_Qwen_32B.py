import pytest
import requests
import logging

test_cases = [
    ("TC_00_CheckConnection", "Is this API working correctly?", 200),
    ("TC_01_ValidRequest", "Hello, how are you?", 200),
    ("TC_02_LongPrompt", "A" * 5000, 200),
    ("TC_03_SpecialCharacters", "What is 2+2? 😊", 200),
    ("TC_04_EmptyPrompt", "", 400),
    ("TC_05_InvalidAPIKey", "Hello", 401),
    ("TC_06_NoAPIKey", "Hello", 401),
]

def build_headers(test_id, config):
    headers = {"Content-Type": "application/json"}
    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_API_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {config['api_key']}"
    return headers

def validate_response(test_id, result):
    assert "choices" in result, f"{test_id}: Response missing 'choices' field"
    assert isinstance(result["choices"], list), f"{test_id}: 'choices' is not a list"
    assert len(result["choices"]) > 0, f"{test_id}: 'choices' is empty"
    assert "message" in result["choices"][0], f"{test_id}: Missing 'message' in first choice"

@pytest.mark.parametrize("test_id, prompt, expected_status", test_cases)
def test_model_api(test_id, prompt, expected_status, config):
    headers = build_headers(test_id, config)

    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model":"Qwen/QwQ-32B",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False,
    }

    logging.info(f"Running {test_id} - Sending request to {config['base_url']}")

    response = requests.post(config['base_url'], headers=headers, json=payload, timeout=20)

    assert response.status_code == expected_status, f"{test_id}: Expected {expected_status}, got {response.status_code}"

    if response.status_code == 200:
        validate_response(test_id, response.json())
