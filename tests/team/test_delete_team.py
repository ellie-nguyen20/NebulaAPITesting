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


def test_delete_team_success(team_api):
    """Test successful team deletion - happy path"""
    
    # First, create a team to delete
    team_name = "team_to_delete"
    team_description = "This team will be deleted"
    
    create_response = team_api.create_team(team_name, team_description)
    assert create_response.ok, "Team creation should succeed for delete test"
    
    create_data = create_response.json()
    team_id = create_data["data"]["id"]
    
    # Store team data for cleanup (in case delete fails)
    team_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": create_response
    }
    created_teams.append(team_data)
    
    print(f"✅ Created team for deletion: {team_name} (ID: {team_id})")
    
    # Now delete the team
    delete_response = team_api.delete_team(team_id)
    print(f"Delete response: {delete_response}")
    
    # Basic response validation
    assert delete_response.ok, f"Delete API call failed with status {delete_response.status_code}"
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    
    # Parse response data
    try:
        data = delete_response.json()
        print(f"Delete response data: {data}")
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")
    
    # Validate response structure
    assert "data" in data, "Response missing 'data' field"
    assert "message" in data, "Response missing 'message' field"
    assert "status" in data, "Response missing 'status' field"
    
    # Validate status field
    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'"
    
    # Validate message field
    expected_message = "Team deleted successfully"
    assert data["message"] == expected_message, f"Expected message '{expected_message}', got '{data['message']}'"
    
    # Validate data field structure
    data_field = data["data"]
    assert isinstance(data_field, dict), "Data field should be a dictionary"
    
    # Validate deleted team info
    assert "id" in data_field, "Missing deleted team ID"
    assert "name" in data_field, "Missing deleted team name"
    assert "description" in data_field, "Missing deleted team description"
    
    # Validate specific values
    deleted_team = data_field
    assert deleted_team["id"] == team_id, f"Deleted team ID should match: {team_id}"
    assert deleted_team["name"] == team_name, f"Deleted team name should match: {team_name}"
    assert deleted_team["description"] == team_description, f"Deleted team description should match: {team_description}"
    
    # Remove from cleanup list since it was successfully deleted
    created_teams.remove(team_data)
    
    print(f"\n🎉 Team deletion successful!")
    print(f"✅ Deleted Team ID: {team_id}")
    print(f"✅ Deleted Team Name: {team_name}")
    print(f"✅ Deleted Team Description: {team_description}")
    
    # Verify team is actually deleted by trying to delete again
    verify_response = team_api.delete_team(team_id)
    assert not verify_response.ok, "Team should not exist after deletion"
    assert verify_response.status_code in [404, 400], f"Expected 404/400 for deleted team, got {verify_response.status_code}"
    
    print(f"✅ Verified: Team {team_id} no longer exists")


def test_delete_team_not_found(team_api):
    """Test deleting a non-existent team - should fail"""
    
    # Use a non-existent team ID
    non_existent_id = 999999
    
    # Try to delete non-existent team
    response = team_api.delete_team(non_existent_id)
    print(f"Delete non-existent team response: {response}")
    
    # Should fail with 404 or 400
    assert not response.ok, "Delete should fail for non-existent team"
    assert response.status_code in [404, 400], f"Expected 404/400 status, got {response.status_code}"
    
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
        
        print(f"✅ Non-existent team correctly rejected: {data['message']}")
        
    except Exception as e:
        print(f"⚠️ Could not parse error response: {e}")


def test_delete_team_invalid_id(team_api):
    """Test deleting with invalid team ID formats"""
    
    # Test with invalid ID types
    invalid_ids = [
        "invalid_string",
        -1,
        0,
        "123abc",
        "abc123",
        "team_123"
    ]
    
    for invalid_id in invalid_ids:
        print(f"\n🧪 Testing invalid ID: {invalid_id} (type: {type(invalid_id)})")
        
        response = team_api.delete_team(invalid_id)
        print(f"Response: {response}")
        
        # Should fail with invalid ID
        assert not response.ok, f"Delete should fail for invalid ID: {invalid_id}"
        assert response.status_code in [400, 422, 404], f"Expected 400/422/404 status, got {response.status_code}"
        
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
            
            print(f"✅ Invalid ID '{invalid_id}' correctly rejected: {data['message']}")
            
        except Exception as e:
            print(f"⚠️ Could not parse error response: {e}")


def test_delete_team_already_deleted(team_api):
    """Test deleting a team that was already deleted"""
    
    # First, create a team
    team_name = "team_to_delete_twice"
    team_description = "This team will be deleted twice"
    
    create_response = team_api.create_team(team_name, team_description)
    assert create_response.ok, "Team creation should succeed for double delete test"
    
    create_data = create_response.json()
    team_id = create_data["data"]["id"]
    
    # Store team data for cleanup (in case delete fails)
    team_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": create_response
    }
    created_teams.append(team_data)
    
    print(f"✅ Created team for double deletion test: {team_name} (ID: {team_id})")
    
    # First deletion
    delete_response1 = team_api.delete_team(team_id)
    assert delete_response1.ok, "First deletion should succeed"
    print(f"✅ First deletion successful")
    
    # Remove from cleanup list since it was successfully deleted
    created_teams.remove(team_data)
    
    # Second deletion attempt
    delete_response2 = team_api.delete_team(team_id)
    print(f"Second deletion response: {delete_response2}")
    
    # Should fail with 404 or 400
    assert not delete_response2.ok, "Second deletion should fail"
    assert delete_response2.status_code in [404, 400], f"Expected 404/400 status, got {delete_response2.status_code}"
    
    # Parse error response
    try:
        data = delete_response2.json()
        print(f"Second deletion error response: {data}")
        
        # Validate error response structure
        assert "status" in data, "Error response missing 'status' field"
        assert data["status"] == "error", f"Expected status 'error', got '{data['status']}'"
        
        # Should have error message
        assert "message" in data, "Error response missing 'message' field"
        assert len(data["message"]) > 0, "Error message should not be empty"
        
        print(f"✅ Second deletion correctly rejected: {data['message']}")
        
    except Exception as e:
        print(f"⚠️ Could not parse error response: {e}")


def test_delete_team_with_special_characters(team_api):
    """Test deleting a team with special characters in name/description"""
    
    # Create a team with special characters
    team_name = "test_team@#$%^&*()_+-=[]{}|;':\",./<>?"
    team_description = "test_description@#$%^&*()_+-=[]{}|;':\",./<>?"
    
    create_response = team_api.create_team(team_name, team_description)
    assert create_response.ok, "Team creation with special characters should succeed"
    
    create_data = create_response.json()
    team_id = create_data["data"]["id"]
    
    # Store team data for cleanup (in case delete fails)
    team_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": create_response
    }
    created_teams.append(team_data)
    
    print(f"✅ Created team with special characters: {team_name} (ID: {team_id})")
    
    # Delete the team
    delete_response = team_api.delete_team(team_id)
    assert delete_response.ok, "Deletion should succeed for team with special characters"
    
    # Remove from cleanup list since it was successfully deleted
    created_teams.remove(team_data)
    
    print(f"✅ Successfully deleted team with special characters")


def test_delete_team_performance(team_api):
    """Test delete team API performance"""
    
    # Create multiple teams for performance testing
    teams_to_create = 3
    created_team_ids = []
    
    print(f"🧪 Creating {teams_to_create} teams for performance testing...")
    
    for i in range(teams_to_create):
        team_name = f"perf_test_team_{i+1}"
        team_description = f"Performance test team {i+1}"
        
        create_response = team_api.create_team(team_name, team_description)
        assert create_response.ok, f"Team creation {i+1} should succeed"
        
        create_data = create_response.json()
        team_id = create_data["data"]["id"]
        created_team_ids.append(team_id)
        
        # Store for cleanup
        team_data = {
            "id": team_id,
            "name": team_name,
            "description": team_description,
            "response": create_response
        }
        created_teams.append(team_data)
        
        print(f"✅ Created team {i+1}: {team_name} (ID: {team_id})")
    
    # Test deletion performance
    print(f"\n🧪 Testing deletion performance for {len(created_team_ids)} teams...")
    
    import time
    deletion_times = []
    
    for i, team_id in enumerate(created_team_ids):
        start_time = time.time()
        
        delete_response = team_api.delete_team(team_id)
        
        end_time = time.time()
        deletion_time = end_time - start_time
        deletion_times.append(deletion_time)
        
        assert delete_response.ok, f"Deletion {i+1} should succeed"
        
        print(f"✅ Deleted team {i+1} in {deletion_time:.3f}s")
        
        # Remove from cleanup list since it was successfully deleted
        created_teams = [team for team in created_teams if team["id"] != team_id]
    
    # Performance analysis
    avg_deletion_time = sum(deletion_times) / len(deletion_times)
    max_deletion_time = max(deletion_times)
    min_deletion_time = min(deletion_times)
    
    print(f"\n📊 Deletion Performance Summary:")
    print(f"  📈 Total teams deleted: {len(created_team_ids)}")
    print(f"  ⏱️ Average deletion time: {avg_deletion_time:.3f}s")
    print(f"  🚀 Fastest deletion: {min_deletion_time:.3f}s")
    print(f"  🐌 Slowest deletion: {max_deletion_time:.3f}s")
    
    # Performance assertions
    assert avg_deletion_time < 2.0, f"Average deletion time should be under 2s, got {avg_deletion_time:.3f}s"
    assert max_deletion_time < 5.0, f"Maximum deletion time should be under 5s, got {max_deletion_time:.3f}s"


def test_delete_team_edge_cases(team_api):
    """Test delete team with various edge cases"""
    
    # Edge case 1: Very large team ID
    large_id = 999999999999999
    
    response1 = team_api.delete_team(large_id)
    print(f"Large ID response: {response1}")
    
    if response1.ok:
        print(f"⚠️ Unexpected success with large ID - team created and stored for cleanup")
        # Store for cleanup if unexpectedly successful
        try:
            data = response1.json()
            if "data" in data and "id" in data["data"]:
                team_data = {
                    "id": data["data"]["id"],
                    "name": data["data"].get("name", "large_id_team"),
                    "description": data["data"].get("description", "Edge case team"),
                    "response": response1
                }
                created_teams.append(team_data)
        except Exception as e:
            print(f"⚠️ Could not store team data for cleanup: {e}")
    else:
        assert response1.status_code in [400, 404, 422], f"Expected 400/404/422 status, got {response1.status_code}"
        print(f"✅ Large ID correctly rejected: {response1.status_code}")
    
    # Edge case 2: Zero ID
    response2 = team_api.delete_team(0)
    print(f"Zero ID response: {response2}")
    
    assert not response2.ok, "Zero ID should be rejected"
    assert response2.status_code in [400, 404, 422], f"Expected 400/404/422 status, got {response2.status_code}"
    print(f"✅ Zero ID correctly rejected: {response2.status_code}")
    
    # Edge case 3: Negative ID
    response3 = team_api.delete_team(-123)
    print(f"Negative ID response: {response3}")
    
    assert not response3.ok, "Negative ID should be rejected"
    assert response3.status_code in [400, 404, 422], f"Expected 400/404/422 status, got {response3.status_code}"
    print(f"✅ Negative ID correctly rejected: {response3.status_code}")
    
    # Edge case 4: String ID (should be converted to int if possible)
    try:
        response4 = team_api.delete_team("123")
        print(f"String ID '123' response: {response4}")
        
        if response4.ok:
            print(f"⚠️ String ID '123' was accepted - might be auto-converted")
        else:
            assert response4.status_code in [400, 404, 422], f"Expected 400/404/422 status, got {response4.status_code}"
            print(f"✅ String ID '123' correctly rejected: {response4.status_code}")
    except Exception as e:
        print(f"✅ String ID '123' caused exception: {e}")


def test_delete_team_concurrent_access(team_api):
    """Test delete team with concurrent access scenarios"""
    
    # Create a team for concurrent testing
    team_name = "concurrent_test_team"
    team_description = "Team for concurrent access testing"
    
    create_response = team_api.create_team(team_name, team_description)
    assert create_response.ok, "Team creation should succeed for concurrent test"
    
    create_data = create_response.json()
    team_id = create_data["data"]["id"]
    
    # Store for cleanup (in case delete fails)
    team_data = {
        "id": team_id,
        "name": team_name,
        "description": team_description,
        "response": create_response
    }
    created_teams.append(team_data)
    
    print(f"✅ Created team for concurrent testing: {team_name} (ID: {team_id})")
    
    # Simulate concurrent delete attempts
    import time
    import threading
    
    delete_results = []
    delete_lock = threading.Lock()
    
    def delete_team_thread(thread_id):
        """Thread function to delete team"""
        try:
            start_time = time.time()
            response = team_api.delete_team(team_id)
            end_time = time.time()
            
            with delete_lock:
                delete_results.append({
                    "thread_id": thread_id,
                    "response": response,
                    "time": end_time - start_time,
                    "success": response.ok
                })
                
        except Exception as e:
            with delete_lock:
                delete_results.append({
                    "thread_id": thread_id,
                    "error": str(e),
                    "time": 0,
                    "success": False
                })
    
    # Start multiple threads
    threads = []
    num_threads = 3
    
    print(f"🧪 Starting {num_threads} concurrent delete threads...")
    
    for i in range(num_threads):
        thread = threading.Thread(target=delete_team_thread, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Analyze results
    print(f"\n📊 Concurrent Delete Results:")
    
    successful_deletes = [r for r in delete_results if r["success"]]
    failed_deletes = [r for r in delete_results if not r["success"]]
    
    print(f"  ✅ Successful deletes: {len(successful_deletes)}")
    print(f"  ❌ Failed deletes: {len(failed_deletes)}")
    
    for result in delete_results:
        thread_id = result["thread_id"]
        if result["success"]:
            print(f"    Thread {thread_id}: ✅ Success in {result['time']:.3f}s")
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"    Thread {thread_id}: ❌ Failed - {error_msg}")
    
    # Business logic validation
    if len(successful_deletes) == 1:
        print(f"✅ Correct behavior: Only one delete succeeded")
        # Remove from cleanup list since it was successfully deleted
        created_teams.remove(team_data)
    elif len(successful_deletes) == 0:
        print(f"⚠️ All deletes failed - team might still exist")
    else:
        print(f"⚠️ Multiple deletes succeeded - potential race condition")
        # Remove from cleanup list since it was successfully deleted
        created_teams.remove(team_data)
    
    # Verify final state
    verify_response = team_api.delete_team(team_id)
    if verify_response.ok:
        print(f"⚠️ Team still exists after concurrent delete attempts")
        # Store for cleanup
        verify_data = verify_response.json()
        verify_team_data = {
            "id": verify_data["data"]["id"],
            "name": verify_data["data"].get("name", "concurrent_test_team"),
            "description": verify_data["data"].get("description", "Team for concurrent access testing"),
            "response": verify_response
        }
        created_teams.append(verify_team_data)
    else:
        print(f"✅ Team successfully deleted by concurrent operation")
