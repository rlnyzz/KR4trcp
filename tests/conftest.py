import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.dependencies import clear_db
from faker import Faker

fake = Faker()

@pytest.fixture(autouse=True)
def clean_db():
    """Автоматическая очистка БД перед каждым тестом"""
    clear_db()
    yield
    clear_db()

@pytest.fixture
async def async_client():
    """Асинхронный клиент для тестов (без запуска сервера)"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def fake_user_data():
    """Генерация случайных валидных данных через Faker"""
    return {
        "username": fake.user_name(),
        "age": fake.random_int(min=18, max=100)
    }

@pytest.fixture
def fake_user_data_edge():
    """Граничные значения"""
    return {
        "username": "a",  # минимальная длина 2, но проверим
        "age": 150
    }