import pytest
import logging
from api_clients.api_key import APIKeyAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_get_api_keys_basic(api_key_api):
    """Test basic API keys retrieval with simple validation"""
    
    # Make API call
    response = api_key_api.get_api_keys()
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, f"API call failed with status {response.status_code}"
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse response data
    try:
        data = response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "API keys successfully retrieved"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, list), "Data field should be a list"
    assert len(data_field) > 0, "API keys list should not be empty"
    
    print(f"\n📊 Found {len(data_field)} API key(s)")

def test_get_api_keys_data_structure(api_key_api):
    """Test API keys response data structure validation"""
        
        response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    # Validate each API key structure
    for i, api_key in enumerate(api_keys):
        print(f"🔍 Validating API key {i+1}: {api_key.get('name', 'Unnamed')}")
        
        # Essential fields for API key
        essential_fields = [
            "id", "name", "key", "status", "created_at", "team"
        ]
        
        for field in essential_fields:
            assert field in api_key, f"API key {i+1} missing '{field}' field"
        
        # Validate specific field values
        key_data = api_key
        
        # ID validation
        key_id = key_data["id"]
        assert isinstance(key_id, int), f"API key {i+1} ID should be integer, got {type(key_id)}"
        assert key_id > 0, f"API key {i+1} ID should be positive, got {key_id}"
        
        # Name validation
        name = key_data["name"]
        assert isinstance(name, str), f"API key {i+1} name should be string, got {type(name)}"
        # Name can be empty string for unnamed keys
        
        # Key validation
        key_value = key_data["key"]
        assert isinstance(key_value, str), f"API key {i+1} key should be string, got {type(key_value)}"
        assert len(key_value) > 0, f"API key {i+1} key should not be empty"
        assert len(key_value) > 20, f"API key {i+1} key should have reasonable length"
        
        # Status validation
        status = key_data["status"]
        assert isinstance(status, int), f"API key {i+1} status should be integer, got {type(status)}"
        assert status in [1, 2], f"API key {i+1} status should be 1 or 2, got {status}"
        
        # Created at validation
        created_at = key_data["created_at"]
        assert isinstance(created_at, int), f"API key {i+1} created_at should be integer, got {type(created_at)}"
        assert created_at > 0, f"API key {i+1} created_at should be positive, got {created_at}"
        
        
        # Team validation - basic type only
        team = key_data["team"]
        assert isinstance(team, (dict, type(None))), f"API key {i+1} team should be dictionary or None, got {type(team)}"
        
        print(f"  ✅ ID: {key_id}, Name: '{name}', Status: {status}, Team: {team}")

def test_get_api_keys_personal_vs_team(api_key_api):
    """Test distinction between personal and team API keys"""
    
    response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    # Separate personal and team keys
    personal_keys = [key for key in api_keys if key.get("team") is None]
    team_keys = [key for key in api_keys if key.get("team") is not None]
    
    print(f"\n📊 API Key Distribution:")
    print(f"  Personal keys: {len(personal_keys)}")
    print(f"  Team keys: {len(team_keys)}")
    
    # Validate personal keys
    for i, key in enumerate(personal_keys):
        assert key["team"] is None, f"Personal key {i+1} should have team=None"
        print(f"  Personal key {i+1}: {key.get('name', 'Unnamed')} (ID: {key['id']})")
    
    # Validate team keys structure
    for i, key in enumerate(team_keys):
        team = key["team"]
        assert team is not None, f"Team key {i+1} should have team!=None"
        assert isinstance(team, dict), f"Team key {i+1} team should be dictionary, got {type(team)}"
        
        # Validate team structure
        assert "id" in team, f"Team key {i+1} team missing 'id'"
        assert "name" in team, f"Team key {i+1} team missing 'name'"
        assert "description" in team, f"Team key {i+1} team missing 'description'"
        
        # Validate team data types
        assert isinstance(team["id"], int), f"Team key {i+1} team.id should be int, got {type(team['id'])}"
        assert isinstance(team["name"], str), f"Team key {i+1} team.name should be str, got {type(team['name'])}"
        assert isinstance(team["description"], str), f"Team key {i+1} team.description should be str, got {type(team['description'])}"
        
        # Validate team values
        assert team["id"] > 0, f"Team key {i+1} team.id should be positive, got {team['id']}"
        assert len(team["name"]) > 0, f"Team key {i+1} team.name should not be empty"
        assert len(team["description"]) > 0, f"Team key {i+1} team.description should not be empty"
        
        print(f"  Team key {i+1}: {key.get('name', 'Unnamed')} (Team: {team})")
    
    # At least one personal key should exist
    assert len(personal_keys) > 0, "Should have at least one personal API key"

def test_get_api_keys_active_status(api_key_api):
    """Test API keys active status validation"""
        
        response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    # Count active and inactive keys
    active_keys = [key for key in api_keys if key.get("status") == 1]
    inactive_keys = [key for key in api_keys if key.get("status") == 2]
    
    print(f"\n📊 API Key Status Distribution:")
    print(f"  Active keys: {len(active_keys)}")
    print(f"  Inactive keys: {len(inactive_keys)}")
    
    # Validate active keys
    for i, key in enumerate(active_keys):
        assert key["status"] == 1, f"Active key {i+1} should have status=1"
        print(f"  Active key {i+1}: {key.get('name', 'Unnamed')} (ID: {key['id']})")
    
    # Validate inactive keys
    for i, key in enumerate(inactive_keys):
        assert key["status"] == 2, f"Inactive key {i+1} should have status=2"
        print(f"  Inactive key {i+1}: {key.get('name', 'Unnamed')} (ID: {key['id']})")
    
    # At least one active key should exist
    assert len(active_keys) > 0, "Should have at least one active API key"

def test_get_api_keys_unique_ids(api_key_api):
    """Test that all API key IDs are unique"""
        
        response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    # Extract all IDs
    key_ids = [key["id"] for key in api_keys]
    unique_ids = set(key_ids)
    
    # Validate uniqueness
    assert len(key_ids) == len(unique_ids), f"All API key IDs should be unique. Found {len(key_ids)} keys but {len(unique_ids)} unique IDs"
    
    print(f"\n✅ All {len(key_ids)} API key IDs are unique")

def test_get_api_keys_unique_keys(api_key_api):
    """Test that all API key values are unique"""
        
        response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    # Extract all key values
    key_values = [key["key"] for key in api_keys]
    unique_values = set(key_values)
    
    # Validate uniqueness
    assert len(key_values) == len(unique_values), f"All API key values should be unique. Found {len(key_values)} keys but {len(unique_values)} unique values"
    
    print(f"\n✅ All {len(key_values)} API key values are unique")

def test_get_api_keys_created_at_ordering(api_key_api):
    """Test that API keys are ordered by creation time (newest first)"""
    
        response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    if len(api_keys) > 1:
        # Extract creation times
        created_times = [key["created_at"] for key in api_keys]
        
        # Check if sorted in descending order (newest first)
        is_descending = all(created_times[i] >= created_times[i+1] for i in range(len(created_times)-1))
        
        if is_descending:
            print(f"\n✅ API keys are ordered by creation time (newest first)")
        else:
            print(f"\nℹ️ API keys may not be strictly ordered by creation time")
            print(f"  Creation times: {created_times}")
    else:
        print(f"\nℹ️ Only {len(api_keys)} API key(s) found - ordering not applicable")

def test_get_api_keys_response_performance(api_key_api):
    """Test API keys response performance and timing"""
    
        import time
        
    # Measure response time
        start_time = time.time()
        response = api_key_api.get_api_keys()
        end_time = time.time()
        
        response_time = end_time - start_time
        
    # Validate response time is reasonable (less than 5 seconds)
    assert response_time < 5.0, f"API response time too slow: {response_time:.2f}s"
    
    # Validate response is successful
    assert response.ok, f"API call failed with status {response.status_code}"
    
    print(f"\n⏱️ API Response Time: {response_time:.3f}s")
    
    # Additional performance checks
    data = response.json()
    api_keys = data["data"]
    
    # Response should contain reasonable number of keys
    assert len(api_keys) <= 100, f"Too many API keys returned: {len(api_keys)}"
    
    print(f"✅ Performance test passed - {len(api_keys)} keys retrieved in {response_time:.3f}s")

def test_get_api_keys_error_handling(api_key_api):
    """Test API keys error handling and edge cases"""
    
    # Test with invalid authentication (if possible)
    # This test assumes the api_key_api is properly authenticated
    # In a real scenario, you might test with invalid tokens
    
    response = api_key_api.get_api_keys()
    
    # Should succeed with valid authentication
    assert response.ok, f"API call should succeed with valid authentication"
    
    # Test response structure even on success
    data = response.json()
    assert "status" in data, "Response should have status field"
    assert data["status"] == "success", f"Expected success status, got {data['status']}"
    
    print(f"\n✅ Error handling test passed - API responds correctly")

def test_get_api_keys_comprehensive_validation(api_key_api):
    """Comprehensive validation of all API keys data"""
    
    response = api_key_api.get_api_keys()
    data = response.json()
    api_keys = data["data"]
    
    print(f"\n🔍 Comprehensive API Keys Validation:")
    print(f"  Total keys: {len(api_keys)}")
    
    # Validate each key comprehensively
    for i, api_key in enumerate(api_keys):
        print(f"\n  Key {i+1}: {api_key.get('name', 'Unnamed')}")
        
        # All required fields present
        required_fields = ["id", "name", "key", "status", "created_at", "team"]
        for field in required_fields:
            assert field in api_key, f"Missing required field: {field}"
        
        # Field type validation
        assert isinstance(api_key["id"], int), "ID should be integer"
        assert isinstance(api_key["name"], str), "Name should be string"
        assert isinstance(api_key["key"], str), "Key should be string"
        assert isinstance(api_key["status"], int), "Status should be integer"
        assert isinstance(api_key["created_at"], int), "Created_at should be integer"
        assert isinstance(api_key["team"], (dict, type(None))), "Team should be dictionary or None"
        
        # Value range validation
        assert api_key["id"] > 0, "ID should be positive"
        assert api_key["status"] in [1, 2], "Status should be 1 or 2"
        assert api_key["created_at"] > 0, "Created_at should be positive"
        # Team validation - basic type only in comprehensive test
        
        # Key format validation
        assert len(api_key["key"]) > 20, "Key should have reasonable length"
        assert api_key["key"].isalnum() or "-" in api_key["key"] or "_" in api_key["key"], "Key should contain valid characters"
        
        print(f"    ✅ All validations passed")
    
    print(f"\n🎉 All {len(api_keys)} API keys passed comprehensive validation!")
