import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def participant_setup():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"
    activity = activities[activity_name]
    activity["participants"].append(email)

    yield activity_name, email

    if email in activity["participants"]:
        activity["participants"].remove(email)


def test_unregister_participant_removes_email_from_activity(client, participant_setup):
    # Arrange
    activity_name, email = participant_setup
    activity = activities[activity_name]
    assert email in activity["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activity["participants"]
