from starlette.testclient import TestClient

from .routes import pets_router

# just a comment

client = TestClient(pets_router)

pets_ids = []
pet_guero = {
    "kind": "Dog",
    "states": [
        "Bad",
        "Underfed",
        "Injured"
    ],
    "location": "fake st. 123, Springfield, California",
    "name": "Guero",
}


def _insert_pet():
    response = client.post("/", json=pet_guero)
    response_data = response.json()
    if response_data.get("id_", False):
        pets_ids.append(response_data["id_"])
    return response


def test_add_a_pets():
    response = _insert_pet()
    assert response.status_code == 201, "Not able to ADD a new pet"


def test_get_all_pets():
    response = client.get("/")
    assert response.status_code == 200, "Not able to GET pets"


def test_get_a_pet_by_id():
    if not pets_ids:
        _insert_pet()
    assert bool(pets_ids), "Not able to ADD a new pet to later GET it by ID"

    response = client.get(f"/{pets_ids[0]}")
    assert response.status_code == 200, "Not able to GET pet by ID"


def test_update_a_pet_by_id():
    if not pets_ids:
        _insert_pet()
    assert bool(pets_ids), "Not able to ADD a new pet to later UPDATE on it"

    pet_oddy = dict(pet_guero)
    pet_oddy.update({"name": "Oddy"})

    response = client.put(f"/{pets_ids[0]}", json=pet_oddy)
    assert response.status_code == 200, "Not able to UPDATE pet"


def test_delete_a_pets():
    if not pets_ids:
        _insert_pet()
    assert bool(pets_ids), "Not able to ADD a new pet to later DELETION"

    for index, pet in enumerate(pets_ids):
        response = client.delete(f"/{pet}")
        assert response.status_code == 200, "Not able to DELETE a pet by ID"
        del pets_ids[index]
