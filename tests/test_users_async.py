import pytest
from app.dependencies import db

pytestmark = pytest.mark.asyncio

class TestUsersAsync:
    """Группа асинхронных тестов для пользователей"""
    
    async def test_create_user_success(self, async_client, fake_user_data):
        """Создание пользователя → 201, проверка структуры ответа"""
        response = await async_client.post("/users", json=fake_user_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert "id" in data
        assert data["username"] == fake_user_data["username"]
        assert data["age"] == fake_user_data["age"]
        assert isinstance(data["id"], int)
    
    async def test_create_user_invalid_age_negative(self, async_client):
        """Создание с отрицательным возрастом → 422"""
        response = await async_client.post("/users", json={
            "username": "testuser",
            "age": -5
        })
        assert response.status_code == 422
    
    async def test_create_user_invalid_age_too_high(self, async_client):
        """Создание с возрастом > 150 → 422"""
        response = await async_client.post("/users", json={
            "username": "testuser",
            "age": 200
        })
        assert response.status_code == 422
    
    async def test_create_user_username_too_short(self, async_client):
        """Имя слишком короткое → 422"""
        response = await async_client.post("/users", json={
            "username": "a",
            "age": 25
        })
        assert response.status_code == 422
    
    async def test_get_existing_user(self, async_client, fake_user_data):
        """Получение существующего пользователя → 200"""
        # Сначала создаём
        create_resp = await async_client.post("/users", json=fake_user_data)
        user_id = create_resp.json()["id"]
        
        # Получаем
        response = await async_client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == fake_user_data["username"]
        assert data["age"] == fake_user_data["age"]
    
    async def test_get_nonexistent_user(self, async_client):
        """Получение несуществующего пользователя → 404"""
        response = await async_client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    async def test_delete_existing_user(self, async_client, fake_user_data):
        """Удаление существующего пользователя → 204"""
        # Создаём
        create_resp = await async_client.post("/users", json=fake_user_data)
        user_id = create_resp.json()["id"]
        
        # Удаляем
        response = await async_client.delete(f"/users/{user_id}")
        assert response.status_code == 204
        
        # Проверяем, что пользователя больше нет
        get_response = await async_client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    async def test_delete_twice_same_user(self, async_client, fake_user_data):
        """Повторное удаление того же пользователя → 404"""
        # Создаём
        create_resp = await async_client.post("/users", json=fake_user_data)
        user_id = create_resp.json()["id"]
        
        # Первое удаление
        response1 = await async_client.delete(f"/users/{user_id}")
        assert response1.status_code == 204
        
        # Второе удаление
        response2 = await async_client.delete(f"/users/{user_id}")
        assert response2.status_code == 404
    
    async def test_delete_nonexistent_user(self, async_client):
        """Удаление несуществующего пользователя → 404"""
        response = await async_client.delete("/users/99999")
        assert response.status_code == 404
    
    async def test_get_all_users_after_operations(self, async_client, fake_user_data):
        """Сложный сценарий: создание → получение → удаление"""
        # Создаём двух пользователей
        user1 = await async_client.post("/users", json={"username": "user1", "age": 20})
        user2 = await async_client.post("/users", json={"username": "user2", "age": 30})
        
        user1_id = user1.json()["id"]
        user2_id = user2.json()["id"]
        
        # Получаем первого
        resp1 = await async_client.get(f"/users/{user1_id}")
        assert resp1.status_code == 200
        
        # Удаляем второго
        await async_client.delete(f"/users/{user2_id}")
        
        # Проверяем, что второй исчез
        resp2 = await async_client.get(f"/users/{user2_id}")
        assert resp2.status_code == 404
        
        # А первый остался
        resp3 = await async_client.get(f"/users/{user1_id}")
        assert resp3.status_code == 200
    
    async def test_create_user_with_faker_edge_values(self, async_client):
        """Граничные значения через Faker"""
        # Минимальный возраст
        resp_min = await async_client.post("/users", json={
            "username": fake.user_name(),
            "age": 0
        })
        assert resp_min.status_code == 201
        
        # Максимальный возраст
        resp_max = await async_client.post("/users", json={
            "username": fake.user_name(),
            "age": 150
        })
        assert resp_max.status_code == 201