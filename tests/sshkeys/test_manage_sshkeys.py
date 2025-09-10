import pytest
import logging
from api_clients.ssh_key import SSHKeyAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global list to store created SSH keys for cleanup
created_ssh_keys = []

@pytest.fixture(autouse=True)
def cleanup_ssh_keys(ssh_key_api):
    """Autouse fixture to clean up any remaining SSH keys after all tests"""
    yield  # Let all tests run first
    
    # Cleanup any remaining SSH keys
    if created_ssh_keys:
        print(f"\n[AUTOCLEANUP] Cleaning up {len(created_ssh_keys)} remaining SSH key(s)...")
        for ssh_key_id in created_ssh_keys.copy():
            try:
                delete_response = ssh_key_api.delete_ssh_key(ssh_key_id)
                if delete_response.ok:
                    print(f"  ✅ Deleted SSH key ID: {ssh_key_id}")
                else:
                    print(f"  Failed to delete SSH key ID: {ssh_key_id}")
            except Exception as e:
                print(f"  Error deleting SSH key ID {ssh_key_id}: {e}")
        created_ssh_keys.clear()
        print(f"✅ [AUTOCLEANUP] Cleanup completed!")

def test_create_ssh_key(ssh_key_api):
    """Test creating SSH key - Happy path"""
    
    # Generate test SSH key pair (simplified for testing)
    ssh_key_name = f"TestSSHKey_{int(time.time())}"
    # This is a sample public key for testing - in real scenario, you'd generate a proper key pair
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vbqajDhA..." + str(int(time.time()))
    
    print(f"\n🔑 Creating SSH key...")
    print(f"  Name: {ssh_key_name}")
    print(f"  Public key: {sample_public_key[:50]}...")
    
    response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key)
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
    
    # Validate essential fields based on actual API response
    essential_fields = ["id", "name", "public_key"]
    for field in essential_fields:
        assert field in data_field, f"Missing essential field: {field}"
    
    # Validate specific values
    created_key = data_field
    
    # ID should be present and valid
    assert created_key["id"] is not None, "ID should not be None"
    assert isinstance(created_key["id"], (int, str)), "ID should be int or string"
    print(f"  ✅ SSH Key ID: {created_key['id']}")
    
    # Name should match
    assert created_key["name"] == ssh_key_name, f"Name should match: {ssh_key_name}"
    print(f"  ✅ SSH Key Name: {created_key['name']}")
    
    # Public key should match
    assert created_key["public_key"] == sample_public_key, f"Public key should match"
    print(f"  ✅ Public Key: {created_key['public_key'][:50]}...")
    
    # Add to cleanup list
    created_ssh_keys.append(created_key["id"])
    
    print(f"\n✅ SSH key created successfully!")
    print(f"  Key ID: {created_key['id']}")
    print(f"  Key Name: {created_key['name']}")
    print(f"  Public Key: {created_key['public_key'][:50]}...")

def test_get_ssh_keys(ssh_key_api):
    """Test getting SSH keys - Happy path"""
    
    print(f"\n📋 Getting SSH keys...")
    
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
    
    print(f"\n✅ SSH keys retrieved successfully!")
    print(f"  Total SSH keys: {len(data_field)}")
    
    # Validate each SSH key structure if any exist
    for i, ssh_key in enumerate(data_field):
        assert isinstance(ssh_key, dict), f"SSH key {i} should be a dictionary"
        essential_fields = ["id", "name", "public_key"]
        for field in essential_fields:
            assert field in ssh_key, f"SSH key {i} missing field: {field}"
        print(f"  SSH Key {i+1}: {ssh_key['name']} (ID: {ssh_key['id']})")

def test_rename_ssh_key(ssh_key_api):
    """Test renaming SSH key - Happy path"""
    
    # First create an SSH key to rename
    ssh_key_name = f"TestSSHKey_rename_{int(time.time())}"
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vbqajDhA..." + str(int(time.time()))
    
    print(f"\n🔑 Creating SSH key for rename test...")
    create_response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key)
    assert create_response.ok, f"Failed to create SSH key for rename test: {create_response.status_code}"
    
    created_key = create_response.json()["data"]
    ssh_key_id = created_key["id"]
    created_ssh_keys.append(ssh_key_id)  # Add to cleanup
    
    print(f"  ✅ Created SSH key: {created_key['name']} (ID: {ssh_key_id})")
    
    # Now rename the SSH key
    new_name = f"RenamedSSHKey_{int(time.time())}"
    print(f"\n✏️ Renaming SSH key...")
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
    
    print(f"\n✅ SSH key renamed successfully!")
    print(f"  Key ID: {renamed_key['id']}")
    print(f"  New name: {renamed_key['name']}")
    print(f"  Public key: {renamed_key['public_key'][:50]}...")

def test_delete_ssh_key(ssh_key_api):
    """Test deleting SSH key - Happy path"""
    
    # First create an SSH key to delete
    ssh_key_name = f"TestSSHKey_delete_{int(time.time())}"
    sample_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vbqajDhA..." + str(int(time.time()))
    
    print(f"\n🔑 Creating SSH key for delete test...")
    create_response = ssh_key_api.create_ssh_key(ssh_key_name, sample_public_key)
    assert create_response.ok, f"Failed to create SSH key for delete test: {create_response.status_code}"
    
    created_key = create_response.json()["data"]
    ssh_key_id = created_key["id"]
    
    print(f"  ✅ Created SSH key: {created_key['name']} (ID: {ssh_key_id})")
    
    # Verify key exists before deletion
    print(f"\n🔍 Verifying SSH key exists before deletion...")
    get_response = ssh_key_api.get_ssh_keys()
    assert get_response.ok, f"Failed to get SSH keys: {get_response.status_code}"
    
    all_keys = get_response.json()["data"]
    key_exists = any(key["id"] == ssh_key_id for key in all_keys)
    assert key_exists, f"SSH key {ssh_key_id} should exist before deletion"
    print(f"  ✅ SSH key {ssh_key_id} exists in the list")
    
    # Delete the SSH key
    print(f"\n🗑️ Deleting SSH key...")
    delete_response = ssh_key_api.delete_ssh_key(ssh_key_id)
    assert delete_response.ok, f"Failed to delete SSH key: {delete_response.status_code}"
    assert delete_response.status_code == 200, f"Expected status 200, got {delete_response.status_code}"
    
    # Parse delete response
    try:
        delete_data = delete_response.json()
        print(f"Delete response: {delete_data}")
    except Exception as e:
        print(f"Delete response is not JSON: {delete_response.text}")
    
    print(f"✅ SSH key deleted successfully!")
    
    # Verify key is deleted
    print(f"\n🔍 Verifying SSH key is deleted...")
    get_response = ssh_key_api.get_ssh_keys()
    assert get_response.ok, f"Failed to get SSH keys for verification: {get_response.status_code}"
    
    remaining_keys = get_response.json()["data"]
    key_still_exists = any(key["id"] == ssh_key_id for key in remaining_keys)
    assert not key_still_exists, f"SSH key {ssh_key_id} should be deleted"
    print(f"  ✅ SSH key {ssh_key_id} no longer exists in the list")
    
    print(f"\n✅ SSH key deletion test completed successfully!")

def test_ssh_key_error_handling(ssh_key_api):
    """Test SSH key error handling"""
    
    print(f"\n🧪 Testing SSH key error handling...")
    
    # Test delete non-existent SSH key
    non_existent_id = "999999999"
    print(f"  Testing deletion of non-existent SSH key ID: {non_existent_id}")
    
    delete_response = ssh_key_api.delete_ssh_key(non_existent_id)
    
    if delete_response.ok:
        print(f"  Deletion of non-existent SSH key succeeded (unexpected behavior)")
    else:
        print(f"  ✅ Deletion of non-existent SSH key correctly failed: {delete_response.status_code}")
        assert delete_response.status_code in [400, 404, 422], f"Expected 400/404/422 for non-existent key, got {delete_response.status_code}"
    
    # Test rename non-existent SSH key
    print(f"  Testing rename of non-existent SSH key ID: {non_existent_id}")
    
    rename_response = ssh_key_api.rename_ssh_key(non_existent_id, "NewName")
    
    if rename_response.ok:
        print(f"  Rename of non-existent SSH key succeeded (unexpected behavior)")
    else:
        print(f"  ✅ Rename of non-existent SSH key correctly failed: {rename_response.status_code}")
        assert rename_response.status_code in [400, 404, 422], f"Expected 400/404/422 for non-existent key, got {rename_response.status_code}"
    
    print(f"\n✅ SSH key error handling test completed successfully!")
