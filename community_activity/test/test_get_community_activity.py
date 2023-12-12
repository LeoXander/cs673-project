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

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Unable to connect to server")
    return responses

@pytest.fixture
def check_top_rows():
    return 10

@pytest.fixture
def required_fields():
    fields = []
    fields.append('communityActivityId')
    fields.append('communityActivityName')
    fields.append('hours')
    fields.append('objectives')
    fields.append('outcomes')
    fields.append('issueAreaID')
    fields.append('issueAreaName')
    fields.append('primaryEntities')
    fields.append('activityTypes')
    return fields

def test_status_codes(response, error_responses):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        assert response.status_code == 404
        response_details = response.json()
        assert response_details['detail'] in error_responses

def test_response_count(response, community_activity_count):
    """
    Test possible no of responses that are expected
    """
    if response.status_code == 200:
        response_details = response.json()
        assert response_details is not None
        assert community_activity_count == len(response_details['communityActivities'])

def test_required_fields(response, check_top_rows, required_fields):
    """
    Test required fields exists and are populared in the responses
    """
    if response.status_code == 200:
        response_details = response.json()
        if len(response_details['communityActivities']) < check_top_rows:
            check_top_rows = len(response_details['communityActivities'])
        for iter_i in range(check_top_rows):
            for field in response_details['communityActivities'][iter_i]:
                assert field in required_fields
