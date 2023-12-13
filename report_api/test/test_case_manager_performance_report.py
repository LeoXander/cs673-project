from fastapi.testclient import TestClient
import pytest
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Case Managers API Error")
    return responses

@pytest.fixture
def response():
    response = client.get("/casemanagerperformancereport")
    return response

@pytest.fixture
def required_fields():
    fields = {}
    fields['caseManagers'] = []
    fields['caseManagers'].append('id')
    fields['caseManagers'].append('CaseManagerName')
    fields['caseManagers'].append('Department')
    fields['caseManagers'].append('ContactNumber')
    fields['caseManagers'].append('casesAssigned')
    return fields

@pytest.fixture
def check_top_rows():
    return 10

def test_status_codes(response, error_responses):
    """Test valid response codes that is acceptable for the API to deploy"""
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        response_details = response.json()
        assert response_details['detail'] in error_responses
        assert response.status_code == 404

def test_required_fields(response, required_fields, check_top_rows):
    if response.status_code == 200:
        response_details = response.json()
        if len(response_details['caseManagers']) < check_top_rows:
            check_top_rows = len(response_details['caseManagers'])
        assert all([field in required_fields['caseManagers'] 
                    for iter_i in range(check_top_rows) 
                    for field in response_details['caseManagers'][iter_i]])



