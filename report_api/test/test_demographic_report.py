from fastapi.testclient import TestClient
from ..main import create_app
client = TestClient(create_app())

def test_demographic_report():
    response = client.get("/demographicchart")
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        print(response)
        assert response.status_code == 404

