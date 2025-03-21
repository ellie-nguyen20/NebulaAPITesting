from serverless_api.base_test import NEBULA_API_KEY, TEXT_API_URL, test_results
import requests
import pytest
import logging


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
    headers = {"Content-Type": "application/json"}

    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "max_tokens": None,
        "temperature": 1,
        "top_p": 0.9,
        "stream": False,
    }

    logging.info(f"Running {test_id} - Sending request to {TEXT_API_URL}")

    try:
        response = requests.post(TEXT_API_URL, headers=headers, json=data, timeout=20)

        if response.status_code != expected_status:
            pytest.fail(
                f"{test_id} ❌ Failed! Expected {expected_status}, got {response.status_code}"
            )

        if response.status_code == 200:
            result = response.json()
            missing_fields = []

            if "choices" not in result:
                missing_fields.append("'choices' field")
            elif not isinstance(result["choices"], list) or not result["choices"]:
                missing_fields.append("'choices' field is empty")
            if "message" not in result["choices"][0]:
                missing_fields.append("'message' field")

            if missing_fields:
                pytest.fail(
                    f"{test_id} ❌ Failed! Response missing: {', '.join(missing_fields)}"
                )

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        pytest.fail(f"{test_id} ❌ Failed! Unexpected error: {e}", pytrace=True)
