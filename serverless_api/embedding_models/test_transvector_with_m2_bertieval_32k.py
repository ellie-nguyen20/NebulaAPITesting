import pytest
import requests

test_cases = [
    ("TC_00_CheckConnection", ["Test connection"], 200),
    ("TC_01_ValidRequest", ["Bananas are berries, but strawberries are not."], 200),
    ("TC_02_EmptyInput", [""], 200),
    ("TC_03_SpecialCharacters", ["!@#$%^&*()_+=-"], 200),
    ("TC_04_LongText", ["This is a long text. " * 500], 200),
    ("TC_05_InvalidAPIKey", ["Invalid API Key test"], 401),
    ("TC_06_NoAPIKey", ["No API Key test"], 401),
]

def build_headers(test_id, config):
    headers = {"Content-Type": "application/json"}
    if test_id == "TC_05_InvalidAPIKey":
        headers["Authorization"] = "Bearer INVALID_API_KEY"
    elif test_id != "TC_06_NoAPIKey":
        headers["Authorization"] = f"Bearer {config['api_key']}"
    return headers

def validate_response(test_id, result):
    assert "data" in result, f"{test_id}: Response missing 'data' field"
    assert isinstance(result["data"], list), f"{test_id}: 'data' is not a list"
    assert "embedding" in result["data"][0], f"{test_id}: Missing 'embedding' in data"

@pytest.mark.parametrize("test_id, input_text, expected_status", test_cases)
def test_nebula_embedding_api(test_id, input_text, expected_status, config):
    headers = build_headers(test_id, config)

    payload = {"model": "togethercomputer/m2-bert-80M-32k-retrieval", "input": input_text}

    response = requests.post( config["embedding_base_url"], headers=headers, json=payload, timeout=20)

    assert response.status_code == expected_status, f"{test_id}: Expected {expected_status}, got {response.status_code}"

    if response.status_code == 200:
        validate_response(test_id, response.json())
