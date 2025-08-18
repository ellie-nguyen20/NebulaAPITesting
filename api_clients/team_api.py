from .base_api import BaseAPIClient

class TeamAPI(BaseAPIClient):
    """Team API client for managing team operations."""

    def create_team(self, name: str, description: str):
        """Create a new team."""
        payload = {"name": name, "description": description}
        return self.post("/teams", data=payload)
    
    
    def delete_team(self, team_id: str):
        """Delete a team."""
        return self.delete(f"/teams/{team_id}")
    
    def get_team_info(self):
        """Get team information."""
        return self.get("/team/info")
    
    def get_team_members(self):
        """Get team members."""
        return self.get("/team/members")
    
    def add_team_member(self, email: str, role: str = "member"):
        """Add a new team member."""
        payload = {"email": email, "role": role}
        return self.post("/team/members", data=payload)
    
    def remove_team_member(self, member_id: str):
        """Remove a team member."""
        return self.delete(f"/team/members/{member_id}")
    
    def update_team_member_role(self, member_id: str, new_role: str):
        """Update team member role."""
        payload = {"role": new_role}
        return self.patch(f"/team/members/{member_id}", data=payload) 