import pytest
from fastapi.testclient import TestClient

from app import cache
from app.main import app

@pytest.fixture(autouse=True)
def clear_cache():
	cache._cache.clear()

	@pytest.fixture
	def client():
		return TestClient(app)