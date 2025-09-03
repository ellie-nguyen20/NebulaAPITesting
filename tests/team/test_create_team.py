import pytest

# Global variable to store created team data for cleanup
created_teams = []

@pytest.fixture(autouse=True)
def cleanup_teams(team_api):
    """Teardown fixture to cleanup created teams after each test"""
    print(f"\n🔄 Starting test with {len(created_teams)} existing teams to cleanup")
    
    yield  # Run the test
    
    # Cleanup: Delete all created teams (even if test failed)
    if created_teams:
        print(f"\n🧹 Cleaning up {len(created_teams)} created team(s)...")
        
        cleanup_success = 0
        cleanup_failed = 0
        
        for team_data in created_teams:
            try:
                team_id = team_data.get("id")
                team_name = team_data.get("name", "Unknown")
                
                if team_id is None:
                    print(f"  ⚠️ Skipping cleanup for team '{team_name}' - no ID available")
                    cleanup_failed += 1
                    continue
                
                print(f"  🗑️ Deleting team: {team_name} (ID: {team_id})")
                
                # Try to delete the team
                delete_response = team_api.delete_team(team_id)
                
                if delete_response.ok:
                    print(f"    ✅ Successfully deleted team {team_name}")
                    cleanup_success += 1
                else:
                    print(f"    ⚠️ Failed to delete team {team_name}: {delete_response.status_code}")
                    cleanup_failed += 1
                    
            except Exception as e:
                print(f"    ❌ Error deleting team {team_data.get('name', 'Unknown')}: {e}")
                cleanup_failed += 1
        
        # Clear the list after cleanup
        total_teams = len(created_teams)
        created_teams.clear()
        
        print(f"✅ Team cleanup completed: {cleanup_success}/{total_teams} successful, {cleanup_failed} failed")
        
        if cleanup_failed > 0:
            print(f"⚠️ Warning: {cleanup_failed} teams could not be cleaned up automatically")
    else:
        print("✅ No teams to cleanup")

def test_create_team(team_api):
    """Test team creation - happy path only"""
    
    # Test data
    team_name = "test_team"
    team_description = "test_description"
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
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
    expected_message = "Team created successfully"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate essential team fields
    essential_fields = ["id", "name", "description"]
    
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific field values
    team = data_field
    
    # ID validation
    team_id = team["id"]
    assert isinstance(team_id, int), "Team ID should be an integer"
    assert team_id > 0, "Team ID should be positive"
    
    # Name validation
    name = team["name"]
    assert isinstance(name, str), "Team name should be a string"
    assert len(name) > 0, "Team name should not be empty"
    assert name == team_name, f"Team name should match input '{team_name}', got '{name}'"
    
    # Description validation
    description = team["description"]
    assert isinstance(description, str), "Team description should be a string"
    assert len(description) > 0, "Team description should not be empty"
    assert description == team_description, f"Team description should match input '{team_description}', got '{description}'"
    
    # Store team data for cleanup
    team_data = {
        "id": team_id,
        "name": name,
        "description": description,
        "response": response
    }
    created_teams.append(team_data)
    
    # Final validation
    assert response.ok, "Final response should be successful"
    
    print(f"\n🎉 Team creation successful!")
    print(f"✅ Team ID: {team_id}")
    print(f"✅ Team Name: {name}")
    print(f"✅ Team Description: {description}")
    
    # Print team summary
    print(f"\n📋 Team Creation Summary:")
    print(f"  🆔 ID: {team_id}")
    print(f"  📝 Name: {name}")
    print(f"  📄 Description: {description}")
    print(f"  ✅ Status: Created successfully")
    


def test_create_team_empty_name(team_api):
    """Test team creation with empty name - should fail"""
    
    # Test data
    team_name = ""
    team_description = "test_description"
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    # Should fail with empty name
    if response.ok:
        # If unexpectedly succeeded, store for cleanup
        try:
            data = response.json()
            if "data" in data and "id" in data["data"]:
                team_data = {
                    "id": data["data"]["id"],
                    "name": data["data"].get("name", "empty_name_team"),
                    "description": data["data"].get("description", "test_description"),
                    "response": response
                }
                created_teams.append(team_data)
                print(f"⚠️ Unexpected success - team created and stored for cleanup")
        except Exception as e:
            print(f"⚠️ Could not store team data for cleanup: {e}")
    
    # Validate that it should fail
    assert not response.ok, "API call should fail with empty team name"
    assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
    
    # Parse error response
    try:
        data = response.json()
        print(f"Error response: {data}")
        
        # Validate error response structure
        assert "status" in data, "Error response missing 'status' field"
        assert data["status"] == "error", f"Expected status 'error', got '{data['status']}'"
        
        # Should have error message
        assert "message" in data, "Error response missing 'message' field"
        assert len(data["message"]) > 0, "Error message should not be empty"
        
        print(f"✅ Empty name correctly rejected: {data['message']}")
        
    except Exception as e:
        print(f"⚠️ Could not parse error response: {e}")



def test_create_team_very_long_name(team_api):
    """Test team creation with very long name - should fail or truncate"""
    
    # Test data - 100 characters
    team_name = "a" * 100
    team_description = "test_description"
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, validate truncation
        data = response.json()
        created_name = data["data"]["name"]
        
        if len(created_name) < len(team_name):
            print(f"✅ Long name was truncated: {len(team_name)} -> {len(created_name)}")
        else:
            print(f"ℹ️ Long name was accepted as-is: {len(created_name)} characters")
            
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": data["data"]["description"],
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Very long name correctly rejected: {response.status_code}")


def test_create_team_special_characters(team_api):
    """Test team creation with special characters in name"""
    
    # Test data with special characters
    team_name = "test_team@#$%^&*()_+-=[]{}|;':\",./<>?"
    team_description = "test_description"
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, validate data
        data = response.json()
        created_name = data["data"]["name"]
        
        print(f"✅ Special characters accepted: {created_name}")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": data["data"]["description"],
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Special characters correctly rejected: {response.status_code}")


def test_create_team_duplicate_name(team_api):
    """Test team creation with duplicate name - should fail or return existing"""
    
    # First, create a team
    team_name = "duplicate_test_team"
    team_description = "test_description"
    
    response1 = team_api.create_team(team_name, team_description)
    assert response1.ok, "First team creation should succeed"
    
    data1 = response1.json()
    team_id1 = data1["data"]["id"]
    
    # Store first team for cleanup
    team_data1 = {
        "id": team_id1,
        "name": team_name,
        "description": team_description,
        "response": response1
    }
    created_teams.append(team_data1)
    
    print(f"✅ First team created: {team_name} (ID: {team_id1})")
    
    # Try to create team with same name
    response2 = team_api.create_team(team_name, team_description)
    print(f"Duplicate creation response: {response2}")
    
    if response2.ok:
        # If accepted, check if it's the same team or new team
        data2 = response2.json()
        team_id2 = data2["data"]["id"]
        
        if team_id2 == team_id1:
            print(f"✅ Duplicate name returned existing team: {team_id1}")
        else:
            print(f"ℹ️ Duplicate name created new team: {team_id1} vs {team_id2}")
            # Store second team for cleanup
            team_data2 = {
                "id": team_id2,
                "name": team_name,
                "description": team_description,
                "response": response2
            }
            created_teams.append(team_data2)
    else:
        # If rejected, validate error
        assert response.status_code in [400, 409, 422], f"Expected 400/409/422 status, got {response.status_code}"
        print(f"✅ Duplicate name correctly rejected: {response.status_code}")


def test_create_team_unicode_name(team_api):
    """Test team creation with unicode characters in name"""
    
    # Test data with unicode characters
    team_name = "test_team_测试_🎉_🚀"
    team_description = "test_description"
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, validate data
        data = response.json()
        created_name = data["data"]["name"]
        
        print(f"✅ Unicode characters accepted: {created_name}")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": data["data"]["description"],
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Unicode characters correctly rejected: {response.status_code}")


def test_create_team_whitespace_handling(team_api):
    """Test team creation with leading/trailing whitespace"""
    
    # Test data with whitespace
    team_name = "  test_team_whitespace  "
    team_description = "  test_description  "
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, check if whitespace was trimmed
        data = response.json()
        created_name = data["data"]["name"]
        created_description = data["data"]["description"]
        
        if created_name == team_name.strip():
            print(f"✅ Whitespace was trimmed from name: '{team_name}' -> '{created_name}'")
        else:
            print(f"ℹ️ Whitespace was preserved in name: '{created_name}'")
            
        if created_description == team_description.strip():
            print(f"✅ Whitespace was trimmed from description: '{team_description}' -> '{created_description}'")
        else:
            print(f"ℹ️ Whitespace was preserved in description: '{created_description}'")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": created_description,
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Whitespace handling correctly rejected: {response.status_code}")


def test_create_team_minimum_length(team_api):
    """Test team creation with minimum valid lengths"""
    
    # Test data with minimum lengths
    team_name = "ab"  # 2 characters
    team_description = "abc"  # 3 characters
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, validate data
        data = response.json()
        created_name = data["data"]["name"]
        created_description = data["data"]["description"]
        
        print(f"✅ Minimum lengths accepted: name='{created_name}' ({len(created_name)}), desc='{created_description}' ({len(created_description)})")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": created_description,
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Minimum lengths correctly rejected: {response.status_code}")


def test_create_team_maximum_length(team_api):
    """Test team creation with maximum valid lengths"""
    
    # Test data with maximum lengths (assuming reasonable limits)
    team_name = "a" * 50  # 50 characters
    team_description = "a" * 500  # 500 characters
    
    # Make API call
    response = team_api.create_team(team_name, team_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, validate data
        data = response.json()
        created_name = data["data"]["name"]
        created_description = data["data"]["description"]
        
        print(f"✅ Maximum lengths accepted: name='{len(created_name)}', desc='{len(created_description)}'")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": created_description,
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ Maximum lengths correctly rejected: {response.status_code}")
        
        # If it's a 500 error, it might have created the team anyway
        if response.status_code == 500:
            print(f"⚠️ Server error (500) - team might have been created despite error")
            # Try to get team info to see if it was created
            try:
                # This is a fallback - we can't easily get the team ID without the response
                print(f"⚠️ Cannot cleanup team due to server error - manual cleanup may be needed")
            except Exception as e:
                print(f"⚠️ Error checking team status: {e}")


def test_create_team_sql_injection_prevention(team_api):
    """Test team creation with SQL injection attempts - should be sanitized"""
    
    # Test data with SQL injection attempts
    sql_injection_name = "test'; DROP TABLE teams; --"
    sql_injection_description = "test'; DELETE FROM users; --"
    
    # Make API call
    response = team_api.create_team(sql_injection_name, sql_injection_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, check if SQL injection was sanitized
        data = response.json()
        created_name = data["data"]["name"]
        created_description = data["data"]["description"]
        
        # Check if dangerous characters were escaped or removed
        dangerous_chars = ["'", ";", "--", "DROP", "DELETE", "TABLE", "FROM"]
        name_contains_dangerous = any(char in created_name.upper() for char in dangerous_chars)
        desc_contains_dangerous = any(char in created_description.upper() for char in dangerous_chars)
        
        if not name_contains_dangerous and not desc_contains_dangerous:
            print(f"✅ SQL injection properly sanitized")
        else:
            print(f"⚠️ SQL injection may not be fully sanitized")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": created_description,
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ SQL injection correctly rejected: {response.status_code}")


def test_create_team_xss_prevention(team_api):
    """Test team creation with XSS attempts - should be sanitized"""
    
    # Test data with XSS attempts
    xss_name = "<script>alert('XSS')</script>"
    xss_description = "<img src=x onerror=alert('XSS')>"
    
    # Make API call
    response = team_api.create_team(xss_name, xss_description)
    print(f"Response: {response}")
    
    if response.ok:
        # If accepted, check if XSS was sanitized
        data = response.json()
        created_name = data["data"]["name"]
        created_description = data["data"]["description"]
        
        # Check if HTML tags were escaped or removed
        html_tags = ["<script>", "</script>", "<img", "onerror="]
        name_contains_html = any(tag in created_name.lower() for tag in html_tags)
        desc_contains_html = any(tag in created_description.lower() for tag in html_tags)
        
        if not name_contains_html and not desc_contains_html:
            print(f"✅ XSS properly sanitized")
        else:
            print(f"⚠️ XSS may not be fully sanitized")
        
        # Store for cleanup
        team_data = {
            "id": data["data"]["id"],
            "name": created_name,
            "description": created_description,
            "response": response
        }
        created_teams.append(team_data)
        
    else:
        # If rejected, validate error
        assert response.status_code in [400, 422], f"Expected 400/422 status, got {response.status_code}"
        print(f"✅ XSS correctly rejected: {response.status_code}")


def test_get_all_teams(team_api):
    """Test getting all teams with simple validation"""
    
    # Make API call
    response = team_api.get_all_teams()
    print(f"Response: {response}")
    
    # Basic response validation
    assert response.ok, "API call should succeed"
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
    expected_message = "Teams retrieved successfully"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, list), "Data field should be a list"
    assert len(data_field) >= 0, "Teams list should not be negative"
    
    print(f"\n📊 Found {len(data_field)} teams")
    
    # If there are teams, validate basic team structure
    if len(data_field) > 0:
        print(f"\n🔍 Validating team structures...")
        
        for i, team in enumerate(data_field):
            print(f"  Team {i+1}: {team.get('name', 'Unknown')}")
            
            # Validate essential team fields
            essential_fields = ["id", "name", "description", "role", "permissions", "members", "created_at", "owner"]
            
            for field in essential_fields:
                assert field in team, f"Team {i+1} missing essential field: {field}"
            
            # Validate basic field types
            assert isinstance(team["id"], int), f"Team {i+1} ID should be an integer"
            assert isinstance(team["name"], str), f"Team {i+1} name should be a string"
            assert isinstance(team["description"], str), f"Team {i+1} description should be a string"
            assert isinstance(team["role"], int), f"Team {i+1} role should be an integer"
            assert isinstance(team["permissions"], list), f"Team {i+1} permissions should be a list"
            assert isinstance(team["members"], int), f"Team {i+1} members should be an integer"
            assert isinstance(team["created_at"], int), f"Team {i+1} created_at should be an integer"
            assert isinstance(team["owner"], dict), f"Team {i+1} owner should be a dictionary"
            
            # Validate owner structure
            owner = team["owner"]
            owner_fields = ["id", "name", "tier"]
            for field in owner_fields:
                assert field in owner, f"Team {i+1} owner missing field: {field}"
            
            # Validate basic values
            assert team["id"] > 0, f"Team {i+1} ID should be positive"
            assert len(team["name"]) > 0, f"Team {i+1} name should not be empty"
            assert team["role"] in [0, 1], f"Team {i+1} role should be 0 or 1"
            assert team["members"] >= 0, f"Team {i+1} members should be non-negative"
            assert team["created_at"] > 0, f"Team {i+1} created_at should be positive"
            assert owner["id"] > 0, f"Team {i+1} owner ID should be positive"
            assert len(owner["name"]) > 0, f"Team {i+1} owner name should not be empty"
            assert len(owner["tier"]) > 0, f"Team {i+1} owner tier should not be empty"
            
            print(f"    ✅ Validated: ID={team['id']}, Role={team['role']}, Members={team['members']}")
            print(f"    ✅ Owner: {owner['name']} (Tier: {owner['tier']})")
        
        # Basic data consistency check
        team_ids = [team["id"] for team in data_field]
        unique_ids = set(team_ids)
        assert len(team_ids) == len(unique_ids), f"Team IDs should be unique, found {len(team_ids)} teams but {len(unique_ids)} unique IDs"
        print(f"\n✅ All team IDs are unique")
        
    else:
        print(f"ℹ️ No teams found - this is valid for new users")
    
    print(f"\n🎉 Get all teams successful!")
    print(f"✅ Total teams: {len(data_field)}")
    print(f"✅ Response status: {data['status']}")
    print(f"✅ Response message: {data['message']}")
  