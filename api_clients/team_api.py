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
    
    def get_all_teams(self):
        """Get all teams."""
        return self.get("/teams")
    
    def get_team(self, team_id: str):
        """Get team information."""
        return self.get(f"/teams/{team_id}")
    
    def get_team_members(self, team_id: str):
        """Get team members."""
        return self.get(f"/teams/{team_id}/members")
    
    def invite_team_member(self, team_id: int, email: str, role: int, permissions: list):
        """Add a new team member."""
        payload = {"email": email, "role": role, "permissions": permissions}
        return self.post(f"/teams/{team_id}/members", data=payload)
    
    def get_invite_info(self, token: str):
        """Get invite info."""
        return self.get(f"/teams/invitations/{token}")
    
    def accept_invite(self, token: str):
        """Accept an invite."""
        return self.post(f"/teams/invitations/{token}")
    
    def remove_team_member(self, member_id: str):
        """Remove a team member."""
        return self.delete(f"/team/members/{member_id}")
    
    def update_team_member_role(self, member_id: str, new_role: str):
        """Update team member role."""
        payload = {"role": new_role}
        return self.patch(f"/team/members/{member_id}", data=payload) 

    def get_teamid_permissions(self, team_id: str):
        """Get team permissions."""
        return self.get(f"/teams/{team_id}/permissions")
    
  