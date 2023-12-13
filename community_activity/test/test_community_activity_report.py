from fastapi.testclient import TestClient
import pytest
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Unable to connect to server")
    return responses

@pytest.fixture
def response():
    response = client.get("/communityactivityeventreport")
    return response

@pytest.fixture
def response_with_date_filter():
    response = client.get("/communityactivityeventreport?startDt=2023-12-13%2000%3A12%3A00&endDt=2023-12-13%2000%3A12%3A00")
    return response

@pytest.fixture
def required_fields():
    fields = {}
    fields['communityActivityReportData'] = []
    fields['communityActivityReportData'].append('issueAreaName')
    fields['communityActivityReportData'].append('activityTypes')
    fields['communityActivityReportData'].append('primaryEntities')
    fields['communityActivityReportData'].append('hours')
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
        if len(response_details['communityActivityReportData']) < check_top_rows:
            check_top_rows = len(response_details['communityActivityReportData'])
        assert all([field in required_fields['communityActivityReportData'] 
                    for iter_i in range(check_top_rows) 
                    for field in response_details['communityActivityReportData'][iter_i]])

def test_status_codes_with_date_filter(response_with_date_filter, error_responses):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    if response_with_date_filter.status_code == 200:
        assert response_with_date_filter.status_code == 200
    else:
        assert response_with_date_filter.status_code == 404
        response_details = response_with_date_filter.json()
        assert response_details['detail'] in error_responses

def test_invalid_filters():
    response = client.get("/communityactivityeventreport?startDt=2023-12-13%2000%3A12%3A00")
    assert response.status_code == 200
    response_details = response.json()
    assert response_details["error"] == "Invalid data entered"