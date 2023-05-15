import json

from fastapi.testclient import TestClient

from .main import app, Category, Item, items


client = TestClient(app)


def test_index():
    response = client.get("/")
    print(response.json())
    print(items)

    assert response.status_code == 200
    assert response.json() == {"items": items}


def test_query_item_by_id():
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == items[0].dict()

    response = client.get("/items/3")
    assert response.status_code == 404


def test_query_item_by_parameters():
    response = client.get("/items/?name=Screws")
    assert response.status_code == 200
    assert len(response.json()["selection"]) == 1
    assert response.json()["selection"][0].name == "Screws"

    response = client.get("/items/?category=tools&price=5.99")
    assert response.status_code == 200
    assert len(response.json()["selection"]) == 1
    assert response.json()["selection"][0].name == "Screwdrivers"

    response = client.get("/items/?count=100")
    assert response.status_code == 200
    assert len(response.json()["selection"]) == 2
    assert all(item.count == 100 for item in response.json()["selection"])

    response = client.get("/items/?name=Hammers&category=consumables&price=9.99&count=100")
    assert response.status_code == 200
    assert len(response.json()["selection"]) == 0


def test_add_item():
    new_item = Item(id=3, name="Drills", category=Category.TOOLS, price=19.99, count=50)
    response = client.post("/", json=new_item.dict())
    assert response.status_code == 200
    assert response.json()["added"] == new_item.dict()

    response = client.post("/", json=new_item.dict())
    assert response.status_code == 400


def test_update_item():
    response = client.put("/items/0", json={"name": "New Hammers"})
    assert response.status_code == 200
    assert response.json()["updated"].name == "New Hammers"

    response = client.put("/items/1", json={"price": 7.99, "count": 50})
    assert response.status_code == 200
    assert response.json()["updated"].price == 7.99
    assert response.json()["updated"].count == 50

    response = client.put("/items/2", json={})
    assert response.status_code == 400

    response = client.put("/items/3", json={"name": "Invalid"})
    assert response.status_code == 404


def test_delete_item():
    response = client.delete("/items/0")
    assert response.status_code == 200
    assert response.json()["deleted"] == items[0].dict()

    response = client.delete("/items/3")
    assert response.status_code == 404
