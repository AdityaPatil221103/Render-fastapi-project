from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#test Home API
def test_home():
    response = client.get("/")
    #Status code check
    assert response.status_code == 200
    #response data check
    assert response.json() == {"message":"hello Aditya"}

#test add API
def test_add():
    response = client.get("/add?a=5&b=4")

    assert response.status_code == 200
    assert response.json() == {"result": 9}