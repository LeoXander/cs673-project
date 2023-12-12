from fastapi.testclient import TestClient
import pytest
from ..main import create_app
client = TestClient(create_app())

@pytest.fixture
def error_responses():
    responses = []
    responses.append("Service Offered API Error")
    responses.append("Bookings API Error")
    responses.append("Vendors API Error")
    return responses

@pytest.fixture
def response():
    response = client.get("/serviceproviderreport")
    return response

@pytest.fixture
def response_of_one_service():
    response = client.get("/serviceproviderreport?serviceName=House%20Cleaning")
    return response

@pytest.fixture
def required_fields():
    fields = {}
    fields['services'] = []
    fields['services'].append('recentVisits')
    fields['services'].append('serviceName')
    fields['services'].append('serviceType')
    fields['services'].append('location')
    fields['services'].append('serviceProviderName')
    fields['services'].append('description')
    fields['recentVisits'] = []
    fields['recentVisits'].append('startTime')
    fields['recentVisits'].append('endTime')
    fields['recentVisits'].append('patientId')
    fields['recentVisits'].append('status')
    fields['recentVisits'].append('remarks')
    return fields

@pytest.fixture
def check_top_rows():
    return 10

def test_status_codes_without_arguments(response, error_responses):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        response_details = response.json()
        assert response_details['detail'] in error_responses
        assert response.status_code == 404

def test_status_codes_with_arguments(response_of_one_service, error_responses):
    """
    Test valid response codes that is acceptable for the API to deploy
    """
    if response_of_one_service.status_code == 200:
        assert response_of_one_service.status_code == 200
    else:
        response_details = response_of_one_service.json()
        assert response_details['detail'] in error_responses
        assert response.status_code == 404

# def test_required_fields()
