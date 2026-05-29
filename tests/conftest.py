import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def clean_activities():
    """Fixture that provides a clean copy of test activities."""
    # Create a minimal test dataset
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["alice@test.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": []
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 2,
            "participants": ["bob@test.edu", "charlie@test.edu"]
        }
    }
    return test_activities


@pytest.fixture
def client(clean_activities):
    """Fixture that provides a test client with clean activities data."""
    # Save original activities
    original_activities = copy.deepcopy(activities)
    
    # Replace with test activities
    activities.clear()
    activities.update(clean_activities)
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)
