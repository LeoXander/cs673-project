from fastapi.testclient import TestClient
import pytest
from ..helpers.dbconnection import *
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def activity_types_count():
    connection = connectToDB()
    cursor = connection.cursor()
    count = 0
    try:
        query = "select count(*) as types_count from activity_types"
        cursor.execute(query)
        count = cursor.fetchone()
        print(count[0])
    except oracledb.Error as e:
        print("Error is connecting and fetching data from db")
        print(str(e))
        assert False
    return count[0]

def test_status_codes(activity_types_count):
    """Test valid response codes that is acceptable for the API to deploy"""
    response = client.get("/activitytypes")
    assert response.status_code == 200
    response_details = response.json()
    assert response_details is not None
    assert activity_types_count == len(response_details['activityTypes'])
    