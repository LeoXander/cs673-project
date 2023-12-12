from fastapi.testclient import TestClient
import pytest
import json
from ..helpers import dbconnection
from ..main import create_app
client = TestClient(create_app())
global ca_id
ca_id = 0
@pytest.fixture(scope="module")
def database_cursor():
    connection = dbconnection.connectToDB()
    cursor = connection.cursor()
    return cursor

@pytest.fixture
def community_activity_id(database_cursor):
    """
    Fixture to get the required data for testing
    """
    count = 0
    value = "Test_event1"
    try:
        query = f"select community_activity_id from community_activities where community_activity_name='{value}'"
        database_cursor.execute(query)
        count = database_cursor.fetchall()
        print(count[0])
    except dbconnection.oracledb.Error as e:
        print("Error in test cases connecting and fetching data from db")
        print(str(e))
        assert False
    print(count)
    return count

@pytest.fixture
def community_activity_data1():
    data = {}
    data["communityEventName"] = "Test_event1"
    data["issueAreaID"] = 14
    data["hours"] = 5
    data["objectives"] = "Test add functionality"
    data["outcomes"] = "Successful addition of functionality"
    data["activityType"] = [5, 6]
    data["primaryEntities"] = [2, 3]
    return data

@pytest.fixture
def community_activity_data2():
    data = {}
    data["communityEventName"] = "Test_event2"
    data["issueAreaID"] = 14
    data["hours"] = 0
    data["objectives"] = "Test add functionality"
    data["outcomes"] = "Successful addition of functionality"
    data["activityType"] = []
    data["primaryEntities"] = [2, 3]
    return data

@pytest.fixture
def valid_response(community_activity_data1):
    """
    Fixture to get the response of the testing module
    """
    response = client.post('/communityactivity',
                           json=json.loads(json.dumps(community_activity_data1)))
    return response

@pytest.fixture
def invalid_response(community_activity_data2):
    """
    Fixture to get the response of the testing module
    """
    response = client.post('/communityactivity',
                           json=json.loads(json.dumps(community_activity_data2)))
    return response

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Unable to connect to server")
    responses.append("The community activity record cannot be added")
    responses.append("Invalid data entered")
    responses.append("The community activity record does not exist")
    return responses

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

def test_valid_response(valid_response):
    """
    Test valid response codes and message that is acceptable for the API to deploy
    """
    assert valid_response.status_code == 201
    response_details = valid_response.json()
    assert response_details['success'] == 1
    assert response_details['message'] == "Community Activity Record inserted successfully"

def test_invalid_response(invalid_response, error_responses):
    """
    Test valid response codes and message that is acceptable for the API to deploy
    """
    assert invalid_response.status_code == 201
    response_details = invalid_response.json()
    assert response_details['error'] in error_responses


def test_community_activity_exists(community_activity_id):
    """
    Test whether the added data exists in the database
    """
    assert community_activity_id != 0

def test_remove_id_verify_data_exists(community_activity_id):
    global ca_id
    for comm_act in community_activity_id:
        response = client.delete(f"/communityactivity/{int(comm_act[0])}")
        assert response.status_code == 200
        response_details = response.json()
        assert response_details['success'] == 1
        assert response_details['message'] == "Community Activity Record deleted successfully"
        ca_id = comm_act[0]
    assert ca_id != 0
    

def test_deleted_event(database_cursor):
    global ca_id
    try:
        query1 = f"select * from community_activities where community_activity_id = {ca_id}"
        query2 = f"select * from activity_areas where community_activity_id = {ca_id}"
        result1 = database_cursor.execute(query1)
        result2 = database_cursor.execute(query2)
        data1 = result1.fetchone()
        data2 = result2.fetchone()
    except dbconnection.oracledb.Error as e:
        print("Error in test cases connecting and fetching data from db")
        print(str(e))
        assert False
    print(data1)
    print(data2)
    assert data1 is None
    assert data2 is None

def test_invalid_delete():
    global ca_id
    assert ca_id != 0
    response = client.delete(f"/communityactivity/{ca_id}")
    assert response.status_code == 200
    response_details = response.json()
    assert response_details['error'] == 'The community activity record does not exist'
