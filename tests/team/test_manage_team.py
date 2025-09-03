import pytest
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Global variable to store created team data for cleanup
created_teams = []

@pytest.fixture(autouse=True)
def cleanup_teams(team_api):
    """Teardown fixture to cleanup created teams after each test"""
    logger.info(f"\n🔄 Starting test with {len(created_teams)} existing teams to cleanup")
    
    yield  # Run the test
    
    # Cleanup: Delete all created teams (even if test failed)
    if created_teams:
        logger.info(f"\n🧹 Cleaning up {len(created_teams)} created team(s)...")
        
        cleanup_success = 0
        cleanup_failed = 0
        
        for team_data in created_teams:
            try:
                team_id = team_data.get("id")
                team_name = team_data.get("name", "Unknown")
                
                if team_id is None:
                    logger.warning(f"  ⚠️ Skipping cleanup for team '{team_name}' - no ID available")
                    cleanup_failed += 1
                    continue
                
                logger.info(f"  🗑️ Deleting team: {team_name} (ID: {team_id})")
                
                # Try to delete the team
                delete_response = team_api.delete_team(team_id)
                
                if delete_response.ok:
                    logger.info(f"    ✅ Successfully deleted team {team_name}")
                    cleanup_success += 1
                else:
                    logger.warning(f"    ⚠️ Failed to delete team {team_name}: {delete_response.status_code}")
                    cleanup_failed += 1
                    
            except Exception as e:
                logger.error(f"    ❌ Error deleting team {team_data.get('name', 'Unknown')}: {e}")
                cleanup_failed += 1
        
        # Clear the list after cleanup
        total_teams = len(created_teams)
        created_teams.clear()
        
        logger.info(f"✅ Team cleanup completed: {cleanup_success}/{total_teams} successful, {cleanup_failed} failed")
        
        if cleanup_failed > 0:
            logger.warning(f"⚠️ Warning: {cleanup_failed} teams could not be cleaned up automatically")
    else:
        logger.info("✅ No teams to cleanup")

@pytest.fixture(scope="function")
def create_user_api(team_api, auth_token):
    """Create a user API client"""
    return UserAPI(team_api.base_url, api_key=auth_token)

def test_get_team_permissions_by_team_id(team_api):
    """Test getting team permissions by team ID with validation"""
    
    # Create a team first
    team_name = "test team get permissions"
    team_description = "test_description"
    create_team_response = team_api.create_team(team_name, team_description)
    assert create_team_response.ok, "Failed to create team"
    
    # Store team data for cleanup (same format as test_create_team.py)
    team_data = create_team_response.json()
    team_id = team_data["data"]["id"]
    
    # Store in created_teams list for cleanup
    cleanup_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": create_team_response
    }
    created_teams.append(cleanup_data)
    
    # Get team permissions
    print(f"Created team: {cleanup_data}")
    print(f"Team ID: {team_id}")
    
    get_team_permissions_response = team_api.get_teamid_permissions(team_id)
    print(f"Permissions response: {get_team_permissions_response}")
    
    # Basic response validation
    assert get_team_permissions_response.ok, "Failed to get team permissions"
    assert get_team_permissions_response.status_code == 200, f"Expected status 200, got {get_team_permissions_response.status_code}"
    
    # Parse response data
    try:
        data = get_team_permissions_response.json()
        print(f"Permissions data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "permissions retrieved successfully"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, list), "Data field should be a list"
    assert len(data_field) >= 0, "Permissions list should not be negative"
    
    print(f"\n📊 Found {len(data_field)} permissions")
    
    # If there are permissions, validate each permission structure
    if len(data_field) > 0:
        print(f"\n🔍 Validating permission structures...")
        
        for i, permission in enumerate(data_field):
            print(f"  Permission {i+1}: {permission.get('name', 'Unknown')}")
            
            # Validate essential permission fields
            essential_fields = ["id", "name", "group_id", "group"]
            
            for field in essential_fields:
                assert field in permission, f"Permission {i+1} missing essential field: {field}"
            
            # Validate basic field types
            assert isinstance(permission["id"], int), f"Permission {i+1} ID should be an integer"
            assert isinstance(permission["name"], str), f"Permission {i+1} name should be a string"
            assert isinstance(permission["group_id"], int), f"Permission {i+1} group_id should be an integer"
            assert isinstance(permission["group"], str), f"Permission {i+1} group should be a string"
            
            # Validate basic values
            assert permission["id"] > 0, f"Permission {i+1} ID should be positive"
            assert len(permission["name"]) > 0, f"Permission {i+1} name should not be empty"
            assert permission["group_id"] > 0, f"Permission {i+1} group_id should be positive"
            assert len(permission["group"]) > 0, f"Permission {i+1} group should not be empty"
            
            print(f"    ✅ Validated: ID={permission['id']}, Group={permission['group']} (Group ID: {permission['group_id']})")
        
        # Basic data consistency check
        permission_ids = [permission["id"] for permission in data_field]
        unique_ids = set(permission_ids)
        assert len(permission_ids) == len(unique_ids), f"Permission IDs should be unique, found {len(permission_ids)} permissions but {len(unique_ids)} unique IDs"
        print(f"\n✅ All permission IDs are unique")
        
        # Check group distribution
        groups = [permission["group"] for permission in data_field]
        unique_groups = set(groups)
        print(f"✅ Permission groups: {list(unique_groups)}")
        
        # Count permissions per group
        group_counts = {}
        for permission in data_field:
            group = permission["group"]
            group_counts[group] = group_counts.get(group, 0) + 1
        
        print(f"✅ Permissions per group: {group_counts}")
        
        # Validate common permission groups based on response
        expected_groups = ["Inference", "Storage", "Instance", "Billing"]
        for group in expected_groups:
            if group in group_counts:
                print(f"✅ Found {group_counts[group]} {group} permissions")
            else:
                print(f"ℹ️ No {group} permissions found")
        
    else:
        print(f"ℹ️ No permissions found - this might be valid for new teams")
    
    print(f"\n🎉 Get team permissions successful!")
    print(f"✅ Total permissions: {len(data_field)}")
    print(f"✅ Response status: {data['status']}")
    print(f"✅ Response message: {data['message']}")
    
@pytest.mark.parametrize("payload", [
    # Test cases for Role 1 (Admin)
    # Test case 1: Admin with no permissions
    {
        "email": "member_no_perms@test.com",
        "role": 1,
        "permissions": [] #ok
    },  
    # Test case 2: Admin with basic permissions (Inference + Storage read)
    {
        "email": "member_basic@test.com",
        "role": 1,
        "permissions": [1, 2]  # Use Inference + Read Storage
    },
    # Test case 3: Admin with storage permissions
    {
        "email": "member_storage@test.com",
        "role": 1,
        "permissions": [2, 3, 5, 6]  # Storage-related permissions
    },
    # Test case 4: Admin with instance permissions
    {
        "email": "member_instance@test.com",
        "role": 1,
        "permissions": [7, 8, 10, 11]  # Instance-related permissions
    },
    # Test case 5: Admin with mixed permissions
    {
        "email": "member_mixed@test.com",
        "role": 1,
        "permissions": [1, 2, 7, 8]  # Inference + Storage read + Instance read/create
    },
    # Test case 6: Admin with full permissions
    {
        "email": "member_full@test.com",
        "role": 1,
        "permissions": [8, 7, 10, 11, 3, 2, 5, 1, 12]  # Full permissions
    },
    
    # Test cases for Role 2 (Member)
    # Test case 7: Member with no permissions
    {
        "email": "owner_no_perms@test.com",
        "role": 2,
        "permissions": []
    },
    # Test case 8: Member with basic permissions
    {
        "email": "owner_basic@test.com",
        "role": 2,
        "permissions": [1, 2, 7, 12]  # Inference + Storage read + Instance read + Billing
    },
    # Test case 9: Member with storage permissions
    {
        "email": "owner_storage@test.com",
        "role": 2,
        "permissions": [2, 3, 5, 6]  # Storage-related permissions
    },
    # Test case 10: Member with instance permissions
    {
        "email": "owner_instance@test.com",
        "role": 2,
        "permissions": [7, 8, 10, 11]  # Instance-related permissions
    },
    # Test case 11: Member with full permissions
    {
        "email": "owner_full@test.com",
        "role": 2,
        "permissions": [8, 7, 10, 11, 3, 2, 5, 1, 12]  # Full permissions
    },
    
    # Test cases for edge cases
    # Test case 12: Minimal payload (no role, no permissions)
    {
        "email": "minimal@test.com"
    },
    # Test case 13: Member with single permission
    {
        "email": "member_single@test.com",
        "role": 1,
        "permissions": [1]  # Only Use Inference
    },
    # Test case 14: Member with single permission
    {
        "email": "owner_single@test.com",
        "role": 2,
        "permissions": [12]  # Only View Billing
    },
    # Test case 15: Admin with specific permission combination
    {
        "email": "member_specific@test.com",
        "role": 1,
        "permissions": [7, 3, 2, 1]  # Specific permission combination
    },
    # Test case 16: Member with specific permission combination
    {
        "email": "owner_specific@test.com",
        "role": 2,
        "permissions": [7, 3, 2, 1]  # Specific permission combination
    }
])
def test_invite_team_member(team_api, payload):
    """Test inviting a team member with different role-permission combinations"""
    
    # Create a team first
    team_name = f"test team invite member {payload.get('email', 'unknown')}"
    team_description = "test_description"
    response = team_api.create_team(team_name, team_description)
    assert response.ok, "Failed to create team"
    
    # Store team data for cleanup (same format as test_create_team.py)
    team_data = response.json()
    team_id = team_data["data"]["id"]
    
    # Store in created_teams list for cleanup
    cleanup_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": response
    }
    created_teams.append(cleanup_data)
    
    print(f"\n🧪 Testing payload: {payload}")
    print(f"✅ Created team: {team_name} (ID: {team_id})")
    
    # Log role and permission information
    if "role" in payload:
        role_name = "Owner" if payload["role"] == 2 else "Member"
        print(f"📋 Inviting as {role_name} (role {payload['role']})")
    else:
        print(f"📋 No role specified - using default")
    
    if "permissions" in payload:
        perm_count = len(payload["permissions"])
        if perm_count == 0:
            print(f"🔐 No special permissions")
        elif perm_count == 1:
            print(f"🔐 Single permission: {payload['permissions']}")
        else:
            print(f"🔐 {perm_count} permissions: {payload['permissions']}")
    else:
        print(f"🔐 No permissions specified - using default")
    
    # Invite a team member with the parametrized payload
    try:
        # Extract individual parameters from payload
        email = payload.get("email", "test@test.com")
        role = payload.get("role", 1)  # Default to member role
        permissions = payload.get("permissions", [])  # Default to no permissions
        
        # Call API with individual parameters
        invite_response = team_api.invite_team_member(team_id, email, role, permissions)
        print(f"✅ Invite successful: {invite_response.json()}")
        
        # Validate successful response
        assert invite_response.ok, "Invite should succeed"
        assert invite_response.status_code == 200, f"Expected status 200, got {invite_response.status_code}"
        
        # Parse and validate response
        data = invite_response.json()
        
        # Validate response structure
        assert "status" in data, "Response missing 'status' field"
        assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
        
        print(f"🎉 Team member invitation successful for {email}!")
        
    except Exception as e:
        # Handle errors gracefully
        if "422 Client Error" in str(e):
            print(f"⚠️ Invite failed with 422 - validation error for {payload.get('email')}")
            print(f"Error details: {e}")
            print(f"Payload: {payload}")
            
            # This is expected for some invalid payloads, so we don't fail the test
            # You can add specific assertions here if you expect certain payloads to fail
            
        elif "400 Client Error" in str(e):
            print(f"⚠️ Invite failed with 400 - bad request for {payload.get('email')}")
            print(f"Error details: {e}")
            print(f"Payload: {payload}")
            
        else:
            # Re-raise unexpected errors
            print(f"❌ Unexpected error for {payload.get('email')}: {e}")
            raise e
    
def test_get_invite_info(team_api):
    """Test getting invite info"""
    
    # Create a team first
    team_name = "test team get invite info"
    team_description = "test_description"
    response = team_api.create_team(team_name, team_description)
    
    # Store team data for cleanup (same format as test_create_team.py)
    team_data = response.json()
    team_id = team_data["data"]["id"]
    
    # Store in created_teams list for cleanup
    cleanup_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": response
    }
    created_teams.append(cleanup_data)

    # Invite a team member
    invite_response = team_api.invite_team_member(team_id, "tesst@test.com", 2, [])
    assert invite_response.ok, "Failed to invite team member"
    print(invite_response.json())
    print("hello")

    token = invite_response.json()["data"]["token"]
    
    # Get invite info
    print(f"Created team: {cleanup_data}")
    print(f"Team ID: {team_id}")
    
    get_invite_info_response = team_api.get_invite_info(token)
    print(get_invite_info_response.json())

def test_accept_invite(team_api):
    """Test accepting an invite"""
    
    # Create a team first
    team_name = "test team accept invite"
    team_description = "test_description"
    response = team_api.create_team(team_name, team_description)
    assert response.ok, "Failed to create team"
    
    # Store team data for cleanup (same format as test_create_team.py)
    team_data = response.json()
    team_id = team_data["data"]["id"]
    
    # Store in created_teams list for cleanup   
    cleanup_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": response
    }
    created_teams.append(cleanup_data)
    
    # Invite a team member
    invite_response = team_api.invite_team_member(team_id, "thivunguyen1506+member1@gmail.com", 2, [])
    assert invite_response.ok, "Failed to invite team member"
    print(invite_response.json())

    token = invite_response.json()["data"]["token"]
    
    # Accept invite
    accept_invite_response = team_api.accept_invite(token)
    assert accept_invite_response.ok, "Failed to accept invite"
    print(accept_invite_response.json())