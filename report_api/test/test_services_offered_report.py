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

def test_status_codes(error_responses):
    """Test valid response codes that is acceptable for the API to deploy"""
    response = client.get("/serviceproviderreport")
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        response_details = response.json()
        assert response_details['detail'] in error_responses
        assert response.status_code == 404

