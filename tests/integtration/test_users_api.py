import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.fixture(scope="session")
def user_data():
    return {}


@pytest.mark.integration
@pytest.mark.asyncio
class TestUserAPI:
    @pytest.mark.dependency()
    async def test_user_create(self, async_client: AsyncClient, user_data):
        mock_data = {
            "email": "api-test@example.com",
            "password": "Secure123!",
        }

        response = await async_client.post("/api/v1/users/", json=mock_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == mock_data["email"]
        assert "id" in data
        user_data["email"] = mock_data["email"]
        user_data["password"] = mock_data["password"]

    @pytest.mark.dependency(["test_user_create"])
    async def test_user_login(self, async_client: AsyncClient, user_data):
        resp = await async_client.post("/api/v1/session/login", json=user_data)

        assert resp.status_code == 204
        assert resp.cookies.get(settings.auth.cookie_name)
        assert resp.cookies.get(settings.auth.device_id_cookie_name)
