from serverless_api.base_test import NEBULA_API_KEY, EMBEDDING_API_URL, test_results
import requests
import pytest
import logging


test_cases = [
    ("TC_00_CheckConnection", ["Test connection"], 200),
    ("TC_01_ValidRequest", ["Bananas are berries, but strawberries are not."], 200),
    ("TC_02_EmptyInput", [""], 200),
    ("TC_03_SpecialCharacters", ["!@#$%^&*()_+=-"], 200),
    ("TC_04_LongText", ["This is a long text. " * 500], 200),
    ("TC_05_InvalidAPIKey", ["Invalid API Key test"], 401),
    ("TC_06_NoAPIKey", ["No API Key test"], 401),
]


@pytest.mark.parametrize("test_id, input_text, expected_status", test_cases)
def test_nebula_embedding_api(test_id, input_text, expected_status):
    headers = {"Content-Type": "application/json"}

    if test_id not in ["TC_05_InvalidAPIKey", "TC_06_NoAPIKey"]:
        headers["Authorization"] = f"Bearer {NEBULA_API_KEY}"

    data = {"model": "WhereIsAI/UAE-Large-V1", "input": input_text}

    logging.info(f"Running {test_id}...")
    try:
        response = requests.post(
            EMBEDDING_API_URL, headers=headers, json=data, timeout=20
        )

        if response.status_code != expected_status:
            pytest.fail(f"Expected {expected_status}, got {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if "data" not in result:
                pytest.fail("Response missing 'data' field.")
            if not isinstance(result["data"], list):
                pytest.fail("Data field is not a list.")
            if "embedding" not in result["data"][0]:
                pytest.fail("Response missing 'embedding' field.")

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        pytest.fail(f"{test_id} ❌ Failed! Unexpected error: {e}", pytrace=True)
