from fastapi.testclient import TestClient
import pytest
from ..helpers import dbconnection
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def community_activity_count():
    """
    Fixture to get the required data for testing
    """
    connection = dbconnection.connectToDB()
    cursor = connection.cursor()
    count = 0
    try:
        query = "select count(*) as community_activity_count from community_activities"
        cursor.execute(query)
        count = cursor.fetchone()
        print(count[0])
    except dbconnection.oracledb.Error as e:
        print("Error in test cases connecting and fetching data from db")
        print(str(e))
        assert False
    return count[0]

@pytest.fixture
def response():
    """
    Fixture to get the response of the testing module
    """
    response = client.get("/communityactivity")
    return response

def test_status_codes(response):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    assert response.status_code == 200

def test_response_count(response, community_activity_count):
    """
    Test possible no of responses that are expected
    """
    response_details = response.json()
    assert response_details is not None
    assert community_activity_count == len(response_details['communityActivities'])

def test_required_fields(response):
    """
    Test required fields exists and are populared in the responses
    """
    response_details = response.json()
    check_top_rows = 10
    count = 0
    for item in response_details['communityActivities']:
        assert 'communityActivityId' in item and item['communityActivityId'] is not None
        assert 'communityActivityName' in item and item['communityActivityName'] is not None
        assert 'hours' in item and item['hours'] is not None
        assert 'objectives' in item and item['objectives'] is not None
        assert 'outcomes' in item and item['outcomes'] is not None
        assert 'issueArea' in item and item['issueArea'] is not None
        assert 'activityTypes' in item and item['activityTypes'] is not None
        count += 1
        if count == check_top_rows:
            break

# Add 404 status code check. Check for proper error message