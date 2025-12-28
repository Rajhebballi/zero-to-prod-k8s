import os

# Set environment variables BEFORE importing the app
os.environ["DB_HOST"] = "test-db"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "test_db"
os.environ["DB_USER"] = "test_user"
os.environ["DB_PASSWORD"] = "test_pass"

from src.app import app

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
