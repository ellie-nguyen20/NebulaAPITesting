from serverless_api.base_test import NEBULA_API_KEY, EMBEDDING_API_URL, test_results
import requests
import pytest
import logging


test_cases = [
    ("TC_00_CheckConnection", ["Test connection"], 200),
    ("TC_01_ValidRequest", ["Bananas are berries, but strawberries are not."], 200),
    ("TC_02_EmptyInput", [""], 400),
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

    data = {
        "model": "WhereIsAI/UAE-Large-V1",
        "input": input_text
    }

    logging.info(f"Running {test_id}...")
    try:
        response = requests.post(EMBEDDING_API_URL, headers=headers, json=data, timeout=20)
        response.raise_for_status()

        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

        if response.status_code == 200:
            result = response.json()
            assert "embeddings" in result, "Response missing 'embeddings' field."
            assert len(result["embeddings"]) == len(input_text), "Mismatch in number of embeddings."

        logging.info(f"{test_id} ✅ Passed!")
        test_results.append((test_id, "✅ Passed", "-"))

    except Exception as e:
        logging.error(f"{test_id} ❌ Failed! Error: {str(e)}")
        test_results.append((test_id, "❌ Failed", str(e)))
