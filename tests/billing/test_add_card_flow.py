import pytest

def test_add_card_flow(credits_api):
    """Test adding a card flow happy path"""
    response = credits_api.add_card()
    assert response.ok, "Failed to add card"
    print(response.json())