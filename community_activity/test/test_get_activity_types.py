from fastapi.testclient import TestClient
import pytest
from ..helpers import dbconnection
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def activity_types_count():
    """
    Fixture to get the required data for testing
    """
    connection = dbconnection.connectToDB()
    cursor = connection.cursor()
    count = 0
    try:
        query = "select count(*) as types_count from activity_types"
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
    response = client.get("/activitytypes")
    return response

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Unable to connect to server")
    return responses

@pytest.fixture
def required_fields():
    fields = []
    fields.append('activityTypeID')
    fields.append('activityTypeName')
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

def test_response_count(response, activity_types_count):
    """
    Test possible no of responses that are expected
    """
    if response.status_code == 200:
        response_details = response.json()
        assert response_details is not None
        assert activity_types_count == len(response_details['activityTypes'])

def test_required_fields(response, required_fields):
    """
    Test required fields exists and are populared in the responses
    """
    if response.status_code == 200:
        response_details = response.json()
        for item in response_details['activityTypes']:
            for key in item:
                assert key in required_fields
                assert item[key] is not None