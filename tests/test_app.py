def test_root_redirect(client):
    """Test root endpoint redirects to static/index.html"""
    # Arrange - no special setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers.get("location", "")


def test_get_activities(client):
    """Test getting all activities"""
    # Arrange - activities are reset by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # From the app, there are 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activity_success(client):
    """Test getting a specific activity successfully"""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get(f"/activities/{activity_name}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Learn strategies and compete in chess tournaments"
    assert "participants" in data
    assert len(data["participants"]) == 2


def test_get_activity_not_found(client):
    """Test getting a non-existent activity"""
    # Arrange
    activity_name = "NonExistent"

    # Act
    response = client.get(f"/activities/{activity_name}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Basketball Team"  # Has empty participants
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    # Verify added to participants
    get_response = client.get(f"/activities/{activity_name}")
    assert email in get_response.json()["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    # Arrange
    activity_name = "Fake Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate(client):
    """Test signup when student already signed up"""
    # Arrange
    activity_name = "Chess Club"  # Has participants
    email = "michael@mergington.edu"  # Already in participants

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_remove_participant_success(client):
    """Test successful removal of participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # In participants

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    # Verify removed
    get_response = client.get(f"/activities/{activity_name}")
    assert email not in get_response.json()["participants"]


def test_remove_activity_not_found(client):
    """Test removal from non-existent activity"""
    # Arrange
    activity_name = "Fake"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_participant_not_found(client):
    """Test removal of participant not in activity"""
    # Arrange
    activity_name = "Basketball Team"  # Empty participants
    email = "notsignedup@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}