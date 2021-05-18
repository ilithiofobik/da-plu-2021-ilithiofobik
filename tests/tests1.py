from datetime import date, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from app import app, Person

client = TestClient(app)


def test1_1():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello world!"}


def test1_2():
    response = client.get("/method")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"method": "GET"}

    response = client.post("/method")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"method": "POST"}

    response = client.delete("/method")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"method": "DELETE"}

    response = client.put("/method")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"method": "PUT"}

    response = client.options("/method")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"method": "OPTIONS"}


def test1_3():
    response = client.get("/auth")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get("/auth?password=haslo")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get("/auth?password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get("/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test1_4():
    response = client.post("/register", json=Person(name="Jan", surname="Nowak").dict())
    assert response.json() == {"id": 1,
                               "name": "Jan",
                               "surname": "Nowak",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(8)).strftime("%Y-%m-%d")}
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/register", json=Person(name="Zofia", surname="Kowalska").dict())
    assert response.json() == {"id": 2,
                               "name": "Zofia",
                               "surname": "Kowalska",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(13)).strftime("%Y-%m-%d")}
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/register", json=Person(name="Janusz", surname="Korwin-Mikke").dict())
    assert response.json() == {"id": 3,
                               "name": "Janusz",
                               "surname": "Korwin-Mikke",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(17)).strftime("%Y-%m-%d")}


def test1_5():
    response = client.get("/patient/1")
    assert response.json() == {"id": 1,
                               "name": "Jan",
                               "surname": "Nowak",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(8)).strftime("%Y-%m-%d")}
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/patient/2")
    assert response.json() == {"id": 2,
                               "name": "Zofia",
                               "surname": "Kowalska",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(13)).strftime("%Y-%m-%d")}
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/patient/3")
    assert response.json() == {"id": 3,
                               "name": "Janusz",
                               "surname": "Korwin-Mikke",
                               "register_date": date.today().strftime("%Y-%m-%d"),
                               "vaccination_date": (date.today() + timedelta(17)).strftime("%Y-%m-%d")}
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/patient/0")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.get("/patient/4")
    assert response.status_code == status.HTTP_404_NOT_FOUND
