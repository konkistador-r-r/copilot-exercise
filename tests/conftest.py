import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

# Original activities data for resetting (captured at import time)
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(scope="function")
def client():
    """FastAPI TestClient fixture for making HTTP requests in tests."""
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_app_state():
    """Reset the global activities dictionary before each test to ensure isolation."""
    global activities
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))