import pytest

# Global variable to store created team data for cleanup
created_teams = []


@pytest.fixture(autouse=True)
def cleanup_teams(team_api):
    """Teardown fixture to cleanup created teams after each test"""
    yield

    if not created_teams:
        print("✅ No teams to cleanup")
        return

    print(f"\n🧹 Cleaning up {len(created_teams)} team(s)...")

    cleanup_success, cleanup_failed, already_deleted = 0, 0, 0

    for team_data in created_teams:
        team_id = team_data.get("id")
        team_name = team_data.get("name", "Unknown")

        if not team_id:
            print(f"  ⚠️ Skipping cleanup for team '{team_name}' - no ID available")
            cleanup_failed += 1
            continue

        try:
            resp = team_api.delete_team(team_id)

            if resp.ok:
                print(f"  ✅ Deleted team {team_name} (ID: {team_id})")
                cleanup_success += 1
            elif resp.status_code in [400, 404]:
                print(f"  ℹ️ Team {team_name} already deleted (status {resp.status_code})")
                already_deleted += 1
            else:
                print(f"  ⚠️ Failed to delete team {team_name}: {resp.status_code}")
                cleanup_failed += 1

        except Exception as e:
            print(f"  ❌ Error deleting team {team_name}: {e}")
            cleanup_failed += 1

    total = len(created_teams)
    created_teams.clear()
    print(f"✅ Cleanup finished: {cleanup_success}/{total} success, {already_deleted} already deleted, {cleanup_failed} failed")


def test_delete_team(team_api):
    """Happy path: Create → Delete → Verify deletion"""

    # --- Setup: create team ---
    team_name = "team_to_delete"
    team_description = "This team will be deleted"

    resp = team_api.create_team(team_name, team_description)
    assert resp.ok, "Team creation failed"

    team = resp.json()["data"]
    team_id = team["id"]
    created_teams.append({"id": team_id, "name": team_name, "description": team_description})
    print(f"✅ Created team: {team_name} (ID: {team_id})")

    # --- Action: delete team ---
    resp = team_api.delete_team(team_id)
    assert resp.ok, f"Delete failed: {resp.status_code}"
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    data = resp.json()
    print(f"Delete response: {data}")

    # --- Assert: response structure ---
    assert data.get("status") == "success"
    assert data.get("message") == "Team deleted successfully"
    assert "data" in data

    if data["data"]:
        # API trả thông tin team sau khi xóa
        deleted = data["data"]
        assert deleted["id"] == team_id
        assert deleted["name"] == team_name
        assert deleted["description"] == team_description
    else:
        print("ℹ️ API returned empty data after deletion")

      # Remove team from cleanup list (already deleted)
    created_teams[:] = [t for t in created_teams if t["id"] != team_id]
