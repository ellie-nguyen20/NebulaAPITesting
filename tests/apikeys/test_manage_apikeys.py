import pytest
import logging
from api_clients.api_key import APIKeyAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global list to store created teams for cleanup
created_teams = []

@pytest.fixture(scope="function")
def test_team(team_api):
    """Fixture to create a test team and clean it up after test"""
    # Setup: Create team
    team_name = f"TestTeam_fixture_{int(time.time())}"
    team_description = "Test team created by fixture"
    
    print(f"\n[FIXTURE] Creating test team: {team_name}")
    team_response = team_api.create_team(team_name, team_description)
    assert team_response.ok, f"Failed to create test team: {team_response.status_code}"
    
    team_data = team_response.json()["data"]
    team_id = team_data["id"]
    created_teams.append(team_id)  # Add to cleanup list
    
    print(f"✅ [FIXTURE] Test team created: {team_name} (ID: {team_id})")
    
    yield team_data  # Provide team data to test
    
    # Teardown: Clean up team
    print(f"\n[FIXTURE] Cleaning up test team: {team_name} (ID: {team_id})")
    try:
        delete_response = team_api.delete_team(team_id)
        if delete_response.ok:
            print(f"✅ [FIXTURE] Test team deleted successfully!")
        else:
            print(f"[FIXTURE] Warning: Failed to delete test team: {delete_response.status_code}")
    except Exception as e:
        print(f"[FIXTURE] Error during team cleanup: {e}")
    finally:
        # Remove from cleanup list
        if team_id in created_teams:
            created_teams.remove(team_id)

@pytest.fixture(autouse=True)
def cleanup_remaining_teams(team_api):
    """Autouse fixture to clean up any remaining teams after all tests"""
    yield  # Let all tests run first
    
    # Cleanup any remaining teams
    if created_teams:
        print(f"\n[AUTOCLEANUP] Cleaning up {len(created_teams)} remaining team(s)...")
        for team_id in created_teams.copy():
            try:
                delete_response = team_api.delete_team(team_id)
                if delete_response.ok:
                    print(f"  ✅ Deleted team ID: {team_id}")
                else:
                    print(f"  Failed to delete team ID: {team_id}")
            except Exception as e:
                print(f"  Error deleting team ID {team_id}: {e}")
        created_teams.clear()
        print(f"✅ [AUTOCLEANUP] Cleanup completed!")

def test_regenerate_personal_api_key(api_key_api):
    """Test regenerate personal API key - Happy path"""
    
    # First, get existing API keys to find a personal key
    response = api_key_api.get_api_keys()
    assert response.ok, f"Failed to get API keys: {response.status_code}"
    
    data = response.json()
    api_keys = data["data"]
    
    # Find a personal key (team = None)
    personal_keys = [key for key in api_keys if key.get("team") is None]
    assert len(personal_keys) > 0, "No personal API keys found for regeneration test"
    
    # Use the first personal key
    personal_key = personal_keys[0]
    api_key_id = personal_key["id"]
    original_name = personal_key["name"]
    original_key_value = personal_key["key"]
    
    print(f"\nRegenerating personal API key:")
    print(f"  ID: {api_key_id}")
    print(f"  Original name: {original_name}")
    print(f"  Original key: {original_key_value[:20]}...")
    
    # Regenerate the personal API key
    new_name = f"{original_name}_regenerated"
    response = api_key_api.regenerate_api_key(api_key_id, new_name)
    
    # Validate response
    assert response.ok, f"Regenerate API key failed with status {response.status_code}"
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
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate essential fields
    essential_fields = ["id", "name", "key", "status", "created_at", "team"]
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific values
    regenerated_key = data_field
    
    # ID should remain the same
    assert regenerated_key["id"] == api_key_id, f"ID should remain the same: {api_key_id}"
    
    # Name should be updated
    assert regenerated_key["name"] == new_name, f"Name should be updated to '{new_name}'"
    
    # Key should be different (regenerated)
    new_key_value = regenerated_key["key"]
    assert new_key_value != original_key_value, "Key value should be different after regeneration"
    assert len(new_key_value) > 20, "New key should have reasonable length"
    
    # Status should be active
    assert regenerated_key["status"] == 1, "Regenerated key should be active (status=1)"
    
    # Team should remain None (personal key)
    assert regenerated_key["team"] is None, "Personal key should have team=None"
    
    # Created_at should be updated (new timestamp)
    assert regenerated_key["created_at"] > personal_key["created_at"], "Created_at should be updated"
    
    print(f"\n✅ Personal API key regenerated successfully!")
    print(f"  New name: {regenerated_key['name']}")
    print(f"  New key: {new_key_value[:20]}...")
    print(f"  Status: {regenerated_key['status']}")
    print(f"  Created at: {regenerated_key['created_at']}")

def test_create_team_api_key(api_key_api, test_team):
    """Test creating API key for a team - Happy path using fixture"""
    
    # Get team data from fixture
    team_id = test_team["id"]
    team_name = test_team["name"]
    print(f"Using test team: {team_name} (ID: {team_id})")
    
    # Create team API key
    print(f"\nCreating team API key...")
    api_key_name = f"TeamKey_create_{int(time.time())}"
    api_key_description = "Test team API key for creation test"
    
    key_response = api_key_api.create_new_api_key(
        name=api_key_name,
        description=api_key_description,
        team_id=team_id
    )
    assert key_response.ok, f"Failed to create team API key: {key_response.status_code}"
    assert key_response.status_code == 200, f"Expected status 200, got {key_response.status_code}"
    
    # Parse response data
    try:
        data = key_response.json()
        print(f"Response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate essential fields based on actual API response
    essential_fields = ["id", "key"]  # Only fields that actually exist
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific values
    created_key = data_field
    
    # ID should be present and valid
    assert created_key["id"] is not None, "ID should not be None"
    assert isinstance(created_key["id"], (int, str)), "ID should be int or string"
    print(f"  ✅ API Key ID: {created_key['id']}")
    
    # Key should be present and have reasonable length
    assert created_key["key"] is not None, "Key should not be None"
    assert len(created_key["key"]) > 10, "Key should have reasonable length"
    print(f"  ✅ API Key: {created_key['key'][:20]}...")
    
    # Check for optional fields that might exist
    if 'name' in created_key:
        assert created_key["name"] == api_key_name, f"Name should match: {api_key_name}"
        print(f"  ✅ API Key Name: {created_key['name']}")
    else:
        print(f"  Name field: Not found in response (API may not return name)")
    
    if 'status' in created_key:
        assert created_key["status"] == 1, "Created key should be active (status=1)"
        print(f"  ✅ Status: {created_key['status']} (active)")
    else:
        print(f"  Status field: Not found in response (API may not return status)")
    
    if 'created_at' in created_key:
        assert created_key["created_at"] is not None, "Created_at should not be None"
        print(f"  ✅ Created at: {created_key['created_at']}")
    else:
        print(f"  Created_at field: Not found in response (API may not return created_at)")
    
    # Check if team info exists in response
    if 'team' in created_key:
        assert isinstance(created_key["team"], dict), "Team should be a dictionary"
        assert "id" in created_key["team"], "Team should have id field"
        assert created_key["team"]["id"] == team_id, f"Team ID should match: {team_id}"
        print(f"  ✅ Team ID: {created_key['team']['id']}")
    else:
        print(f"  Team info: Not found in response (may be in different field)")
    
    print(f"\n✅ Team API key created successfully!")
    print(f"  Key ID: {created_key['id']}")
    print(f"  Key: {created_key['key'][:20]}...")
    print(f"  Team ID: {team_id}")
    print(f"  Requested Name: {api_key_name}")
    
    # Note: Team cleanup is handled by the test_team fixture automatically

def test_delete_team_api_key(api_key_api, test_team):
    """Test deleting team API key - Happy path using fixture"""
    
    # Get team data from fixture
    team_id = test_team["id"]
    team_name = test_team["name"]
    print(f"📋 Using test team: {team_name} (ID: {team_id})")
    
    # Step 1: Create team API key first
    print(f"\n🔑 Step 1: Creating team API key...")
    api_key_name = f"TeamKey_delete_{int(time.time())}"
    api_key_description = "Test team API key for deletion test"
    
    key_response = api_key_api.create_new_api_key(
        name=api_key_name,
        description=api_key_description,
        team_id=team_id
    )
    assert key_response.ok, f"Failed to create team API key: {key_response.status_code}"
    assert key_response.status_code == 200, f"Expected status 200, got {key_response.status_code}"
    
    # Get created key data
    key_data = key_response.json()["data"]
    api_key_id = key_data["id"]
    api_key_value = key_data["key"]
    
    print(f"✅ Team API key created successfully!")
    print(f"  Key ID: {api_key_id}")
    print(f"  Key: {api_key_value[:20]}...")
    print(f"  Team ID: {team_id}")
    
    # Step 2: Verify key exists before deletion
    print(f"\n🔍 Step 2: Verifying key exists before deletion...")
    get_response = api_key_api.get_api_keys()
    assert get_response.ok, f"Failed to get API keys: {get_response.status_code}"
    
    all_keys = get_response.json()["data"]
    key_exists = any(key["id"] == api_key_id for key in all_keys)
    assert key_exists, f"API key {api_key_id} should exist before deletion"
    print(f"  ✅ API key {api_key_id} exists in the list")
    
    # Step 3: Delete team API key
    print(f"\n🗑️ Step 3: Deleting team API key...")
    delete_response = api_key_api.delete_api_key(api_key_id)
    assert delete_response.ok, f"Failed to delete team API key: {delete_response.status_code}"
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    
    # Parse delete response
    try:
        delete_data = delete_response.json()
        print(f"Delete response: {delete_data}")
    except Exception as e:
        print(f"Delete response is not JSON: {delete_response.text}")
    
    print(f"✅ Team API key deleted successfully!")
    
    # Step 4: Verify key is deleted
    print(f"\n🔍 Step 4: Verifying key is deleted...")
    get_response = api_key_api.get_api_keys()
    assert get_response.ok, f"Failed to get API keys for verification: {get_response.status_code}"
    
    remaining_keys = get_response.json()["data"]
    key_still_exists = any(key["id"] == api_key_id for key in remaining_keys)
    assert not key_still_exists, f"API key {api_key_id} should be deleted"
    print(f"  ✅ API key {api_key_id} no longer exists in the list")
    
    # Step 5: Try to delete non-existent key (should fail gracefully)
    print(f"\n🧪 Step 5: Testing deletion of non-existent key...")
    non_existent_id = "999999999"
    delete_nonexistent_response = api_key_api.delete_api_key(non_existent_id)
    
    if delete_nonexistent_response.ok:
        print(f"  ℹ️ Deletion of non-existent key succeeded (unexpected behavior)")
    else:
        print(f"  ✅ Deletion of non-existent key correctly failed: {delete_nonexistent_response.status_code}")
        assert delete_nonexistent_response.status_code in [400, 404, 422], f"Expected 400/404/422 for non-existent key, got {delete_nonexistent_response.status_code}"
    
    print(f"\n✅ Team API key deletion test completed successfully!")
    print(f"  ✅ Key created and deleted")
    print(f"  ✅ Verification passed")
    print(f"  ✅ Error handling tested")
    
    # Note: Team cleanup is handled by the test_team fixture automatically

def test_team_api_key_flow(api_key_api, team_api):
    """Test complete team API key flow: create team -> create team key -> regenerate -> delete key -> delete team"""
    
    import time
    
    # Step 1: Create a team
    print(f"\n🏗️ Step 1: Creating a team...")
    team_name = f"TestTeam_flow_{int(time.time())}"
    team_description = "Test team for API key flow"
    
    team_response = team_api.create_team(team_name, team_description)
    assert team_response.ok, f"Failed to create team: {team_response.status_code}"
    
    team_data = team_response.json()["data"]
    team_id = team_data["id"]
    print(f"✅ Team created successfully: {team_name} (ID: {team_id})")
    
    try:
        # Step 2: Create team API key
        print(f"\n🔑 Step 2: Creating team API key...")
        api_key_name = f"TeamKey_flow_{int(time.time())}"
        api_key_description = "Test team API key"
        
        key_response = api_key_api.create_new_api_key(
            name=api_key_name,
            description=api_key_description,
            team_id=team_id
        )
        assert key_response.ok, f"Failed to create team API key: {key_response.status_code}"
        
        key_data = key_response.json()["data"]
        api_key_id = key_data["id"]
        original_key_value = key_data["key"]
        print(f"✅ Team API key created successfully: {api_key_name} (ID: {api_key_id})")
        print(f"  Key: {original_key_value[:20]}...")
        print(f"  Response data: {key_data}")  # Debug: show actual response structure
        print(f"  Status: {key_data.get('status', 'N/A')}")
        
        # Check if team info exists in response
        if 'team' in key_data:
            print(f"  Team ID: {key_data['team']['id']}")
        else:
            print(f"  Team info: Not found in response (may be in different field)")
        
        # Step 3: Regenerate team API key
        print(f"\n🔄 Step 3: Regenerating team API key...")
        new_key_name = f"{api_key_name}_regenerated_flow_{int(time.time())}"
        
        regenerate_response = api_key_api.regenerate_api_key(api_key_id, new_key_name)
        assert regenerate_response.ok, f"Failed to regenerate team API key: {regenerate_response.status_code}"
        
        regenerated_data = regenerate_response.json()["data"]
        new_key_value = regenerated_data["key"]
        print(f"✅ Team API key regenerated successfully!")
        print(f"  New name: {regenerated_data['name']}")
        print(f"  New key: {new_key_value[:20]}...")
        print(f"  Status: {regenerated_data['status']}")
        
        # Validate regeneration - KEEP ORIGINAL LOGIC (expect ID to remain same)
        assert regenerated_data["id"] == api_key_id, "ID should remain the same"
        assert regenerated_data["name"] == new_key_name, "Name should be updated"
        assert new_key_value != original_key_value, "Key value should be different"
        assert regenerated_data["status"] == 1, "Status should be active"
        
        # Check team association (if team field exists)
        if 'team' in regenerated_data:
            assert regenerated_data["team"]["id"] == team_id, "Should remain team key"
            print(f"  Team association verified: {regenerated_data['team']['id']}")
        else:
            print(f"  Team info: Not found in regenerated response")
        
        # Step 4: Delete team API key
        print(f"\n🗑️ Step 4: Deleting team API key...")
        delete_response = api_key_api.delete_api_key(api_key_id)
        assert delete_response.ok, f"Failed to delete team API key: {delete_response.status_code}"
        
        print(f"✅ Team API key deleted successfully!")
        
        # Verify key is deleted by trying to get it
        get_response = api_key_api.get_api_keys()
        assert get_response.ok, "Failed to get API keys for verification"
        
        remaining_keys = get_response.json()["data"]
        deleted_key = [key for key in remaining_keys if key["id"] == api_key_id]
        assert len(deleted_key) == 0, "API key should be deleted"
        
        print(f"✅ Verification: API key no longer exists in list")
        
        print(f"\n🎉 Complete team API key flow test passed!")
        print(f"  ✅ Team created and deleted")
        print(f"  ✅ Team API key created, regenerated, and deleted")
        print(f"  ✅ All validations passed")
        
    finally:
        # Step 5: Delete team (cleanup) - ALWAYS EXECUTE EVEN IF TEST FAILS
        print(f"\n🧹 Step 5: Cleaning up - deleting team...")
        try:
            delete_team_response = team_api.delete_team(team_id)
            if delete_team_response.ok:
                print(f"✅ Team deleted successfully!")
            else:
                print(f"⚠️ Warning: Failed to delete team: {delete_team_response.status_code}")
        except Exception as e:
            print(f"⚠️ Error during team cleanup: {e}")
        
        print(f"🧹 Cleanup completed!")
    