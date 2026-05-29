"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern."""
import pytest


def test_unregister_removes_participant_successfully(client):
    """Arrange-Act-Assert: Verify participant is successfully removed."""
    # Arrange
    activity_name = "Chess Club"
    email = "alice@test.edu"  # Already in fixture
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_updates_activity_participant_list(client):
    """Arrange-Act-Assert: Verify participant is removed from activity list."""
    # Arrange
    activity_name = "Chess Club"
    email = "alice@test.edu"
    
    # Act
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_fails_for_nonexistent_activity(client):
    """Arrange-Act-Assert: Verify unregister fails with 404 for invalid activity."""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@test.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_fails_for_not_registered_student(client):
    """Arrange-Act-Assert: Verify unregister fails with 400 if not registered."""
    # Arrange
    activity_name = "Programming Class"
    email = "notregistered@test.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_decrements_participant_count(client):
    """Arrange-Act-Assert: Verify participant count decreases after unregister."""
    # Arrange
    activity_name = "Gym Class"
    email = "bob@test.edu"
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity_name]["participants"])
    
    # Act
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    
    # Assert
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity_name]["participants"])
    assert count_after == count_before - 1


def test_unregister_multiple_participants_from_same_activity(client):
    """Arrange-Act-Assert: Verify removing one participant doesn't affect others."""
    # Arrange
    activity_name = "Gym Class"
    email_to_remove = "bob@test.edu"
    email_to_keep = "charlie@test.edu"
    
    # Act
    client.delete(f"/activities/{activity_name}/unregister", params={"email": email_to_remove})
    response = client.get("/activities")
    
    # Assert
    participants = response.json()[activity_name]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants
