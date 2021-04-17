from hashlib import sha512
from typing import Optional
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import date, timedelta

app = FastAPI(
    title="Python Level Up 2021",
    description="Projekt aplikacji na potrzeby kursu Python Level Up 2021.",
)

app.id = 0
app.patients = []


class Person(BaseModel):
    name: str
    surname: str


class Patient(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str


class MessageResp(BaseModel):
    message: str


class MethodResp(BaseModel):
    method: str


# 1.1
@app.get("/", response_model=MessageResp)
def root():
    return MessageResp(message="Hello world!")


# 1.2
@app.get("/method", response_model=MethodResp)
def get_method():
    return MethodResp(method="GET")


@app.post("/method", status_code=status.HTTP_201_CREATED, response_model=MethodResp)
def post_method():
    return MethodResp(method="POST")


@app.delete("/method", response_model=MethodResp)
def delete_method():
    return MethodResp(method="DELETE")


@app.put("/method", response_model=MethodResp)
def put_method():
    return MethodResp(method="PUT")


@app.options("/method", response_model=MethodResp)
def options_method():
    return MethodResp(method="OPTIONS")


# 1.3
@app.get("/auth")
def get_auth(response: Response, password_hash: Optional[str] = None, password: Optional[str] = None):
    response.status_code = status.HTTP_401_UNAUTHORIZED
    if password and password_hash:
        if sha512(password.encode("utf-8")).hexdigest() == password_hash:
            response.status_code = status.HTTP_204_NO_CONTENT


# 1.4
def id_inc():
    app.id += 1
    return app.id


@app.post("/register", response_model=Patient, status_code=status.HTTP_201_CREATED)
def register(person: Person):
    plainname = ''.join(filter(str.isalpha, person.name))
    plainsurname = ''.join(filter(str.isalpha, person.surname))
    new_patient = Patient(id=id_inc(),
                   name=person.name,
                   surname=person.surname,
                   register_date=date.today().strftime("%Y-%m-%d"),
                   vaccination_date=(date.today() + timedelta(days=len(plainname) + len(plainsurname))).strftime("%Y-%m-%d"))

    app.patients.append(new_patient)
    return new_patient


# 1.5
@app.get("/patient/{id}", response_model=Patient)
def patient(id: int, response: Response):
    if id < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    if id > len(app.patients):
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    response.status_code = status.HTTP_200_OK
    return app.patients[id - 1].dict()
