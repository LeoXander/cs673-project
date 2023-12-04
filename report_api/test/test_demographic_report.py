from fastapi import FastAPI
from report_api import main
from fastapi.testclient import TestClient


client = TestClient(main.app)

def test_demographic_report():
    response = client.get("/demographicchart")
    assert response.status_code == 200

