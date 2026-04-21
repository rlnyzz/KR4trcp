import pytest
from app.dependencies import db

pytestmark = pytest.mark.asyncio

class TestUserLifecycle:
    """Тестирование полного жизненного цикла пользователя"""
    
    async def test_full_crud_cycle(self, async_client, fake_user_data):
        """CRUD цикл: Create → Read → Delete"""
        # Create
        create_resp = await async_client.post("/users", json=fake_user_data)
        assert create_resp.status_code == 201
        user_id = create_resp.json()["id"]
        
        # Read
        get_resp = await async_client.get(f"/users/{user_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["username"] == fake_user_data["username"]
        
        # Delete
        del_resp = await async_client.delete(f"/users/{user_id}")
        assert del_resp.status_code == 204
        
        # Verify deleted
        verify_resp = await async_client.get(f"/users/{user_id}")
        assert verify_resp.status_code == 404
    
    async def test_multiple_users_isolation(self, async_client):
        """Проверка изоляции данных между разными пользователями"""
        # Создаём двух разных пользователей
        user_a = await async_client.post("/users", json={"username": "alpha", "age": 25})
        user_b = await async_client.post("/users", json={"username": "beta", "age": 30})
        
        user_a_id = user_a.json()["id"]
        user_b_id = user_b.json()["id"]
        
        # Удаляем только A
        await async_client.delete(f"/users/{user_a_id}")
        
        # A не существует
        resp_a = await async_client.get(f"/users/{user_a_id}")
        assert resp_a.status_code == 404
        
        # B существует
        resp_b = await async_client.get(f"/users/{user_b_id}")
        assert resp_b.status_code == 200
        assert resp_b.json()["username"] == "beta"