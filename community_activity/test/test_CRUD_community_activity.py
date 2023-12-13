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

@pytest.fixture(scope="module")
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
    global ca_id
    for comm_act in community_activity_id:
        assert comm_act[0] != 0
        ca_id = comm_act[0]
    

def test_update_event(community_activity_data1):
    global ca_id
    community_activity_data1["activityType"] = [5]
    community_activity_data1["hours"] = 2
    community_activity_data1["primaryEntities"] = [1, 2]
    response = client.put(f"/communityactivity/{ca_id}",
                          json=json.loads(json.dumps(community_activity_data1)))
    assert response.status_code == 200
    response_details = response.json()
    assert response_details["success"] == 1
    assert response_details["message"] == "Community Activity Record updated successfully"

def test_updated_data(community_activity_data1):
    global ca_id
    getall_response = client.get("/communityactivity")
    assert getall_response.status_code == 200
    response_details = getall_response.json()
    for item in response_details["communityActivities"]:
        if item["communityActivityId"] == ca_id:
            for key in item:
                if key == "communityActivityId":
                    continue
                elif key == "communityActivityName":
                    assert item[key] == community_activity_data1["communityEventName"]
                    continue
                elif key == "issueAreaName":
                    continue
                elif key == "activityTypes":
                    try:
                        for act_type in item[key]:
                            assert act_type["activityTypeID"] in community_activity_data1["activityType"]
                    except Exception as e:
                        print(str(e))
                        assert False
                    continue
                elif key == "primaryEntities":
                    try:
                        for prime_entity in item[key]:
                            assert prime_entity["primaryEntityId"] in community_activity_data1[key]
                    except Exception as e:
                        print(str(e))
                        assert False
                    continue
                assert item[key] == community_activity_data1[key]


def test_remove_id_verify_data_exists(community_activity_id):
    """
    Test deletion of the created activity and validate the responses
    """
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
    """
    Test whether the deleted data is successful by checking the same in the database
    """
    global ca_id
    try:
        query1 = f"select * from community_activities where community_activity_id = {ca_id}"
        query2 = f"select * from activity_areas where community_activity_id = {ca_id}"
        query3 = f"select * from activity_entities where community_activity_id = {ca_id}"
        result1 = database_cursor.execute(query1)
        result2 = database_cursor.execute(query2)
        result3 = database_cursor.execute(query3)
        data1 = result1.fetchone()
        data2 = result2.fetchone()
        data3 = result3.fetchone()
    except dbconnection.oracledb.Error as e:
        print("Error in test cases connecting and fetching data from db")
        print(str(e))
        assert False
    print(data1)
    print(data2)
    assert data1 is None
    assert data2 is None
    assert data3 is None

def test_invalid_delete():
    """

    """
    global ca_id
    assert ca_id != 0
    response = client.delete(f"/communityactivity/{ca_id}")
    assert response.status_code == 200
    response_details = response.json()
    assert response_details['error'] == 'The community activity record does not exist'
