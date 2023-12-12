from fastapi.testclient import TestClient
import pytest
from ..helpers import dbconnection
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def primary_entities_count():
    """
    Fixture to get the required data for testing
    """
    connection = dbconnection.connectToDB()
    cursor = connection.cursor()
    count = 0
    try:
        query = "select count(*) as entities_count from primary_entities"
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
    response = client.get("/primaryentities")
    return response

def test_status_codes(response):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    assert response.status_code == 200

def test_response_count(response, primary_entities_count):
    """
    Test possible no of responses that are expected
    """
    response_details = response.json()
    assert response_details is not None
    assert primary_entities_count == len(response_details['primaryEntities'])

def test_required_fields(response):
    """
    Test required fields exists and are populared in the responses
    """
    response_details = response.json()
    for item in response_details['primaryEntities']:
        assert 'primaryEntityID' in item and item['primaryEntityID'] is not None
        assert 'primaryEntityName' in item and item['primaryEntityName'] is not None


# Add 404 status code check. Check for proper error message
    