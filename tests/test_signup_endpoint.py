"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""
import pytest


def test_signup_adds_participant_successfully(client):
    """Arrange-Act-Assert: Verify a new participant is successfully added."""
    # Arrange
    activity_name = "Programming Class"
    email = "david@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in response.json()["message"]


def test_signup_updates_activity_participant_list(client):
    """Arrange-Act-Assert: Verify participant appears in activity list after signup."""
    # Arrange
    activity_name = "Programming Class"
    email = "eve@test.edu"
    
    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_fails_for_nonexistent_activity(client):
    """Arrange-Act-Assert: Verify signup fails with 404 for invalid activity."""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_signup_fails_for_duplicate_registration(client):
    """Arrange-Act-Assert: Verify signup fails with 400 if already registered."""
    # Arrange
    activity_name = "Chess Club"
    email = "alice@test.edu"  # Already registered in fixture
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_with_special_characters_in_activity_name(client):
    """Arrange-Act-Assert: Verify signup works with encoded activity names."""
    # Arrange
    activity_name = "Programming Class"  # Has space, needs encoding
    email = "frank@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200


def test_signup_increments_participant_count(client):
    """Arrange-Act-Assert: Verify participant count increases after signup."""
    # Arrange
    activity_name = "Programming Class"
    email = "grace@test.edu"
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity_name]["participants"])
    assert count_after == count_before + 1
