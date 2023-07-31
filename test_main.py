import logging

from fastapi import status
from fastapi.testclient import TestClient

from main import app


def create_user(client) -> dict:
    response = client.post("/users", json={"name": "foobar"})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def get_all_users(client) -> dict:
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_user(client, user_id: int):
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_users():
    with TestClient(app) as client:
        # expect nothing in fresh db
        response = get_all_users(client)
        print("TEST USERS", response)
        assert len(response) == 0
        # create an entry
        response = create_user(client)
        user_id = response["id"]
        # get entry
        response = get_all_users(client)
        assert len(response) == 1
        assert response[0]["id"] == user_id
        assert response[0]["name"] == "foobar"
        response = delete_user(client, user_id=user_id)
        response = get_all_users(client)
        assert len(response) == 0


def create_pasture(client, user_id):
    response = client.post(
        "/pasture", json={"name": "Old Millers Pasture", "user_id": user_id}
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def create_pasture_record(client, pasture_id: int, data):
    response = client.post(f"/pasture/{pasture_id}/record", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


def fail_create_pasture_record(client, pasture_id, data):
    response = client.post(f"/pasture/{pasture_id}/record", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def get_pastures(client, user_id):
    response = client.get(f"/pasture/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def get_pasture_records(client, pasture_id):
    response = client.get(f"/pasture/{pasture_id}/record")
    assert response.status_code == status.HTTP_200_OK
    return response.json()


def delete_pasture(client, pasture_id: int):
    response = client.delete(f"/pasture/{pasture_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def delete_pasture_record(client, pasture_id: int, record_id: int):
    response = client.delete(f"/pasture/{pasture_id}/{record_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_crud_pasture():
    with TestClient(app) as client:
        response = create_user(client)
        user_id = response["id"]

        response = create_pasture(client, user_id)
        pasture_id = response["id"]

        response_pasture = get_pastures(client, user_id)

        assert len(response_pasture) == 1
        assert pasture_id == response_pasture[0]["id"]

        pasture_res_1 = create_pasture_record(
            client,
            pasture_id,
            {
                "pasture_id": pasture_id,
                "year": 2020,
            },
        )

        pasture_res_2 = create_pasture_record(
            client,
            pasture_id,
            {
                "pasture_id": pasture_id,
                "year": 2020,
                "tillage_depth": 5.0,
                "tilled": True,
                "external_account_id": "ABc123",
                "crop_type": "Corn",
            },
        )

        # Out of bounds Tillage depth
        fail_create_pasture_record(
            client,
            pasture_id,
            data={
                "pasture_id": pasture_id,
                "year": 2020,
                "tillage_depth": 11.0,
            },
        )

        fail_create_pasture_record(
            client,
            pasture_id,
            data={
                "pasture_id": pasture_id,
                "year": 2020,
                "tillage_depth": -1.0,
            },
        )

        # Out of bounds external_ID
        fail_create_pasture_record(
            client,
            pasture_id,
            data={
                "pasture_id": pasture_id,
                "year": 2020,
                "external_account_id": "ABD###",
            },
        )

        # Crop not in list
        fail_create_pasture_record(
            client,
            pasture_id,
            data={
                "pasture_id": pasture_id,
                "year": 2020,
                "crop_type": "Wheat",
            },
        )

        response_pasture_records = get_pasture_records(client, pasture_id)

        assert len(response_pasture_records) == 2
        assert pasture_res_1["id"] == response_pasture_records[0]["id"]
        assert pasture_res_2["id"] == response_pasture_records[1]["id"]

        delete_pasture_record(client, pasture_id, pasture_res_1["id"])
        delete_pasture_record(client, pasture_id, pasture_res_2["id"])

        response_pasture_records = get_pasture_records(client, pasture_id)
        assert len(response_pasture_records) == 0

        delete_pasture(client, pasture_id)

        response_pastures = get_pastures(client, user_id)
        assert len(response_pastures) == 0

        delete_user(client, user_id)
