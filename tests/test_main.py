from fastapi.testclient import TestClient
from app.main import app, products, customers, orders

client = TestClient(app)


def setup_function():
    products.clear()
    customers.clear()
    orders.clear()


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_create_product():
    response = client.post(
        "/products",
        json={
            "id": 101,
            "name": "MacBook Air",
            "price": 89999,
            "stock": 10
        }
    )

    assert response.status_code == 200
    assert response.json()["product"]["name"] == "MacBook Air"


def test_create_customer():
    response = client.post(
        "/customers",
        json={
            "id": 1,
            "name": "Sapna",
            "email": "sapna@example.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["customer"]["name"] == "Sapna"


def test_create_order():

    client.post(
        "/products",
        json={
            "id": 101,
            "name": "MacBook Air",
            "price": 89999,
            "stock": 10
        }
    )

    client.post(
        "/customers",
        json={
            "id": 1,
            "name": "Sapna",
            "email": "sapna@example.com"
        }
    )

    response = client.post(
        "/orders",
        json={
            "id": 1001,
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2
        }
    )

    assert response.status_code == 200
    assert response.json()["total_amount"] == 179998