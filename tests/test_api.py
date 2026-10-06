import asyncio
from app.main import app
from fastapi.testclient import TestClient

def test_api_endpoints():
    client = TestClient(app)
    
    # Test that the app loads
    response = client.get("/")
    assert response.status_code == 200
    print("✅ Root endpoint works")
    
    # Test that API routes are registered
    response = client.get("/api/docs")
    assert response.status_code == 200
    print("✅ API routes are registered")
    
    print("✅ All basic tests passed!")

if __name__ == "__main__":
    test_api_endpoints()