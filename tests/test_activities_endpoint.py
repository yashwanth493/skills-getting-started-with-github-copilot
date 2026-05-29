"""Tests for GET /activities endpoint using AAA pattern."""
import pytest


def test_get_all_activities_returns_all_activities(client):
    """Arrange-Act-Assert: Verify all activities are returned."""
    # Arrange (setup data - already done by fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_all_activities_contains_required_fields(client):
    """Arrange-Act-Assert: Verify activity objects have required fields."""
    # Arrange (setup data - already done by fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_chess_club_has_one_participant(client):
    """Arrange-Act-Assert: Verify Chess Club has initial participant."""
    # Arrange (setup data - already done by fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    chess_club = activities["Chess Club"]
    assert len(chess_club["participants"]) == 1
    assert "alice@test.edu" in chess_club["participants"]


def test_get_activities_programming_class_empty(client):
    """Arrange-Act-Assert: Verify Programming Class has no participants initially."""
    # Arrange (setup data - already done by fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    prog_class = activities["Programming Class"]
    assert len(prog_class["participants"]) == 0
