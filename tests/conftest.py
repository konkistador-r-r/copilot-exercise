import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

# Original activities data for resetting
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """FastAPI TestClient fixture"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_app_state():
    """Reset the activities dictionary before each test"""
    global activities
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield