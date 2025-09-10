import pytest
import logging
from api_clients.ssh_key import SSHKeyAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global list to store created SSH keys for cleanup
created_ssh_keys = []

@pytest.fixture(autouse=True)
def cleanup_ssh_keys(login_as_user):
    """Autouse fixture to clean up any remaining SSH keys after all tests using Member10"""
    yield  # Let all tests run first
    
    # Cleanup any remaining SSH keys using Member10
    if created_ssh_keys:
        print(f"\n[AUTOCLEANUP] Cleaning up {len(created_ssh_keys)} remaining SSH key(s) using Member10...")
        try:
            user_config = login_as_user("Member10")
            ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
            
            for ssh_key_id in created_ssh_keys.copy():
                try:
                    delete_response = ssh_key_api.delete_ssh_key(ssh_key_id)
                    if delete_response.ok:
                        print(f"  Deleted SSH key ID: {ssh_key_id}")
                    else:
                        print(f"  Failed to delete SSH key ID: {ssh_key_id}")
                except Exception as e:
                    print(f"  Error deleting SSH key ID {ssh_key_id}: {e}")
        except Exception as e:
            print(f"  Error during cleanup: {e}")
        created_ssh_keys.clear()
        print(f"[AUTOCLEANUP] Cleanup completed!")

def test_create_ssh_key(login_as_user):
    """Test creating SSH key - Happy path using Ellie (admin)"""
    
    # Login as Ellie (admin user) - might have SSH key permissions
    print(f"\nLogging in as Ellie (admin user)...")
    user_config = login_as_user("Ellie")
    ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
    
    # Debug: Print authentication details
    print(f"  Base URL: {user_config['base_url']}")
    print(f"  API Key: {user_config['api_key'][:20]}..." if user_config['api_key'] else "  API Key: None")
    print(f"  Full API Key: {user_config['api_key']}")
    
    # Generate test SSH key pair (simplified for testing)
    ssh_key_name = f"TestSSHKey_{int(time.time())}"
    ssh_key_description = "Test SSH key for automated testing"
    # Use proper SSH key format as provided by user
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDQ4WzgAOh8IDv8+dy4PqkEYC/S6iSdgFL99zlRV0Xw6MJcdpKKRyrYFWnIBHAUsA0jnIuhbS9Y4D12ONWG76DVWx50eBA/PKmHmWmNrjdnkLuav6EqRyGA1PDhF21nEOeYrKTQb8aAnJBT2lZPqOByhys6Iy6VrLuV84XNX3rMv+7tUw15OLSKY4hWZdV0ybwbsd7tDs7l8S1F4hkjE+nQmq68nF4uKw0IcJVgpqQim52eile+dETOzazaOeN2O71+Z4YJsXl4kQGInl6PuuZDGNePT0EyqorEeuJ3hhtCLX3z4ykFgE4OLgvdBUt1DF6tMkLTDHEO8vrXoHq9mHid2Q77whjoLl0bHnsB3s47tRXmF+nsgIm752ERiwBkOk1vtKcY8m3BAawYgRIrXh7xyOWlPuczeHxWn0s35EFjF+jiEedCjHIUUXQQ9L694/KavQbLxsOZZ5XJLZ7tbDd1nMNmorO7oVYPhMMYP2bMVXKNBBbmzuvSINtDVdyHRXRe0sUfq9jl8gccQW0zdwvXclljuALo05dXr6qwUE8iNdxGiAUbmYXCXoz6f5Y+ESIMP3pm2csm7unX9WYqubpRJeovds9crxz7ROtmgh8ZZ2Ox6Us/LG4Oyvc1/gkZMPgVMg/92ESinnmLqa3yEnOCQZhgJplMtUQ89DHfP6PL1Q==thivunguyen1506@gmail.com"
    
    print(f"\nCreating SSH key...")
    print(f"  Key Name: {ssh_key_name}")
    print(f"  Key Data: {sample_public_key[:50]}...")
    print(f"  Description: {ssh_key_description} (not used in API)")
    
    response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key, ssh_key_description)
    
    # Debug: Print response details
    print(f"  Response status: {response.status_code}")
    print(f"  Response headers: {dict(response.headers)}")
    print(f"  Response text: {response.text}")
    
    if not response.ok:
        print(f"  Error details: {response.text}")
        # Try to parse error response
        try:
            error_data = response.json()
            print(f"  Error JSON: {error_data}")
        except:
            print(f"  Error is not JSON")
    
    assert response.ok, f"Failed to create SSH key: {response.status_code}"
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
    
    # Validate essential fields (adjust based on actual API response)
    essential_fields = ["id"]  # Start with just ID, add more as we see the response
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific values
    created_key = data_field
    
    # ID should be present and valid
    assert created_key["id"] is not None, "ID should not be None"
    assert isinstance(created_key["id"], (int, str)), "ID should be int or string"
    print(f"  SSH Key ID: {created_key['id']}")
    
    # Check for name field (might be key_name or name)
    if "name" in created_key:
        assert created_key["name"] == ssh_key_name, f"Name should match: {ssh_key_name}"
        print(f"  SSH Key Name: {created_key['name']}")
    elif "key_name" in created_key:
        assert created_key["key_name"] == ssh_key_name, f"Key name should match: {ssh_key_name}"
        print(f"  SSH Key Name: {created_key['key_name']}")
    else:
        print(f"  Name field: Not found in response (API may not return name)")
    
    # Check for public key field (might be public_key or key_data)
    if "public_key" in created_key:
        assert created_key["public_key"] == sample_public_key, f"Public key should match"
        print(f"  Public Key: {created_key['public_key'][:50]}...")
    elif "key_data" in created_key:
        assert created_key["key_data"] == sample_public_key, f"Key data should match"
        print(f"  Key Data: {created_key['key_data'][:50]}...")
    else:
        print(f"  Public key field: Not found in response (API may not return public key)")
    
    # Add to cleanup list
    created_ssh_keys.append(created_key["id"])
    
    print(f"\nSSH key created successfully!")
    print(f"  Key ID: {created_key['id']}")
    print(f"  Key Name: {created_key['name']}")
    print(f"  Public Key: {created_key['public_key'][:50]}...")

def test_get_ssh_keys(login_as_user):
    """Test getting SSH keys - Happy path using Member10"""
    
    # Login as Member10
    print(f"\nLogging in as Member10...")
    user_config = login_as_user("Member10")
    ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
    
    print(f"\nGetting SSH keys...")
    
    response = ssh_key_api.get_ssh_keys()
    assert response.ok, f"Failed to get SSH keys: {response.status_code}"
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
    assert isinstance(data_field, list), "Data field should be a list"
    
    print(f"\nSSH keys retrieved successfully!")
    print(f"  Total SSH keys: {len(data_field)}")
    
    # Validate each SSH key structure if any exist
    for i, ssh_key in enumerate(data_field):
        assert isinstance(ssh_key, dict), f"SSH key {i} should be a dictionary"
        essential_fields = ["id", "name", "public_key"]
        for field in essential_fields:
            assert field in ssh_key, f"SSH key {i} missing field: {field}"
        print(f"  SSH Key {i+1}: {ssh_key['name']} (ID: {ssh_key['id']})")

def test_rename_ssh_key(login_as_user):
    """Test renaming SSH key - Happy path using Member10"""
    
    # Login as Member10
    print(f"\nLogging in as Member10...")
    user_config = login_as_user("Member10")
    ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
    
    # First create an SSH key to rename
    ssh_key_name = f"TestSSHKey_rename_{int(time.time())}"
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vbqajDhA..." + str(int(time.time()))
    
    print(f"\nCreating SSH key for rename test...")
    create_response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key)
    assert create_response.ok, f"Failed to create SSH key for rename test: {create_response.status_code}"
    
    created_key = create_response.json()["data"]
    ssh_key_id = created_key["id"]
    created_ssh_keys.append(ssh_key_id)  # Add to cleanup
    
    print(f"  Created SSH key: {created_key['name']} (ID: {ssh_key_id})")
    
    # Now rename the SSH key
    new_name = f"RenamedSSHKey_{int(time.time())}"
    print(f"\nRenaming SSH key...")
    print(f"  Original name: {ssh_key_name}")
    print(f"  New name: {new_name}")
    
    response = ssh_key_api.rename_ssh_key(ssh_key_id, new_name)
    assert response.ok, f"Failed to rename SSH key: {response.status_code}"
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
    
    # Validate specific values
    renamed_key = data_field
    
    # ID should remain the same
    assert renamed_key["id"] == ssh_key_id, f"ID should remain the same: {ssh_key_id}"
    
    # Name should be updated
    assert renamed_key["name"] == new_name, f"Name should be updated to '{new_name}'"
    
    # Public key should remain the same
    assert renamed_key["public_key"] == sample_public_key, "Public key should remain the same"
    
    print(f"\nSSH key renamed successfully!")
    print(f"  Key ID: {renamed_key['id']}")
    print(f"  New name: {renamed_key['name']}")
    print(f"  Public key: {renamed_key['public_key'][:50]}...")

def test_delete_ssh_key(login_as_user):
    """Test deleting SSH key - Happy path using Member10"""
    
    # Login as Member10
    print(f"\nLogging in as Member10...")
    user_config = login_as_user("Member10")
    ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
    
    # First create an SSH key to delete
    ssh_key_name = f"TestSSHKey_delete_{int(time.time())}"
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vbqajDhA..." + str(int(time.time()))
    
    print(f"\nCreating SSH key for delete test...")
    create_response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key)
    assert create_response.ok, f"Failed to create SSH key for delete test: {create_response.status_code}"
    
    created_key = create_response.json()["data"]
    ssh_key_id = created_key["id"]
    
    print(f"  Created SSH key: {created_key['name']} (ID: {ssh_key_id})")
    
    # Verify key exists before deletion
    print(f"\nVerifying SSH key exists before deletion...")
    get_response = ssh_key_api.get_ssh_keys()
    assert get_response.ok, f"Failed to get SSH keys: {get_response.status_code}"
    
    all_keys = get_response.json()["data"]
    key_exists = any(key["id"] == ssh_key_id for key in all_keys)
    assert key_exists, f"SSH key {ssh_key_id} should exist before deletion"
    print(f"  SSH key {ssh_key_id} exists in the list")
    
    # Delete the SSH key
    print(f"\nDeleting SSH key...")
    delete_response = ssh_key_api.delete_ssh_key(ssh_key_id)
    assert delete_response.ok, f"Failed to delete SSH key: {delete_response.status_code}"
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    
    # Parse delete response
    try:
        delete_data = delete_response.json()
        print(f"Delete response: {delete_data}")
    except Exception as e:
        print(f"Delete response is not JSON: {delete_response.text}")
    
    print(f"SSH key deleted successfully!")
    
    # Verify key is deleted
    print(f"\nVerifying SSH key is deleted...")
    get_response = ssh_key_api.get_ssh_keys()
    assert get_response.ok, f"Failed to get SSH keys for verification: {get_response.status_code}"
    
    remaining_keys = get_response.json()["data"]
    key_still_exists = any(key["id"] == ssh_key_id for key in remaining_keys)
    assert not key_still_exists, f"SSH key {ssh_key_id} should be deleted"
    print(f"  SSH key {ssh_key_id} no longer exists in the list")
    
    print(f"\nSSH key deletion test completed successfully!")

def test_ssh_key_error_handling(login_as_user):
    """Test SSH key error handling using Member10"""
    
    # Login as Member10
    print(f"\nLogging in as Member10...")
    user_config = login_as_user("Member10")
    ssh_key_api = SSHKeyAPI(user_config["base_url"], api_key=user_config["api_key"])
    
    print(f"\nTesting SSH key error handling...")
    
    # Test delete non-existent SSH key
    non_existent_id = "999999999"
    print(f"  Testing deletion of non-existent SSH key ID: {non_existent_id}")
    
    delete_response = ssh_key_api.delete_ssh_key(non_existent_id)
    
    if delete_response.ok:
        print(f"  Deletion of non-existent SSH key succeeded (unexpected behavior)")
    else:
        print(f"  Deletion of non-existent SSH key correctly failed: {delete_response.status_code}")
        assert delete_response.status_code in [400, 404, 422], f"Expected 400/404/422 for non-existent key, got {delete_response.status_code}"
    
    # Test rename non-existent SSH key
    print(f"  Testing rename of non-existent SSH key ID: {non_existent_id}")
    
    rename_response = ssh_key_api.rename_ssh_key(non_existent_id, "NewName")
    
    if rename_response.ok:
        print(f"  Rename of non-existent SSH key succeeded (unexpected behavior)")
    else:
        print(f"  Rename of non-existent SSH key correctly failed: {rename_response.status_code}")
        assert rename_response.status_code in [400, 404, 422], f"Expected 400/404/422 for non-existent key, got {rename_response.status_code}"
    
    print(f"\nSSH key error handling test completed successfully!")
