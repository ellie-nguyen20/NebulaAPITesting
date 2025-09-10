from .base_api import BaseAPIClient

class SSHKeyAPI(BaseAPIClient):
    """SSH Key API client for managing SSH key operations."""

    def create_ssh_key(self, name: str, public_key: str, description: str = ""):
        """Create a new SSH key."""
        payload = {
            "key_name": name,
            "key_data": public_key
        }
        return self.post("/ssh-keys", data=payload)
    
    def get_ssh_keys(self):
        """Get all SSH keys."""
        return self.get("/ssh-keys")
    
    def rename_ssh_key(self, ssh_key_id: str, name: str):
        """Rename an SSH key."""
        payload = {"name": name}
        return self.put(f"/ssh-keys/{ssh_key_id}", data=payload)
    
    def delete_ssh_key(self, ssh_key_id: str):
        """Delete an SSH key."""
        return self.delete(f"/ssh-keys/{ssh_key_id}")
