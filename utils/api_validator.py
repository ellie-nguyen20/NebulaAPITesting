from jsonschema import validate, ValidationError

def validate_status_code(response, expected_code=200):
    actual_code = response.status_code
    assert actual_code == expected_code, \
        f"[Status Code Mismatch] Expected: {expected_code}, Got: {actual_code}"

def validate_json_schema(response, schema):
    try:
        json_data = response.json()
        validate(instance=json_data, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"[Schema Validation Failed] {e.message}")

def validate_required_fields(response, required_fields):
    json_data = response.json()
    missing = [f for f in required_fields if f not in json_data]
    assert not missing, f"[Missing Fields] {missing}" 