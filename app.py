import random
import string
from hashlib import sha512
from typing import Optional
from fastapi import FastAPI, Request, Response, Cookie, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from datetime import date, timedelta
from secrets import compare_digest


app = FastAPI(
    title="Python Level Up 2021",
    description="Projekt aplikacji na potrzeby kursu Python Level Up 2021.",
)

app.id = 0
app.patients = []
app.session_tokens = []
app.tokens = []
app.max_capacity = 1

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


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
                          vaccination_date=(date.today() + timedelta(days=len(plainname) + len(plainsurname))).strftime(
                              "%Y-%m-%d"))

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


# 3.1
@app.get("/hello")
def hello_date(response: Response,request: Request):
    today = date.today().strftime("%Y-%m-%d")
    response.headers["content-type"] = "html"
    return templates.TemplateResponse(
        "hello_date.html.j2",
        {"request": request, "date": today},
    )


# 3.2
def random_token():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(32))


@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, "4dm1n")
    correct_password = compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)

    session_token = random_token()
    response.set_cookie(key="session_token", value=session_token)
    app.session_tokens.append(session_token)

    if len(app.session_tokens) > app.max_capacity:
        app.session_tokens.pop(0)


@app.post("/login_token", status_code=201)
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, "4dm1n")
    correct_password = compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401)

    session_token = random_token()
    app.tokens.append(session_token)  # dodawanie login token

    if len(app.tokens) > app.max_capacity:
        app.tokens.pop(0)

    return {"token": session_token}


# 3.3
@app.get("/welcome_session", status_code=200)
def welcome_session(response: Response, session_token: str = Cookie(None), format: str = ""):
    if (session_token not in app.session_tokens) or (session_token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")

    if format == 'json':
        return {"message": "Welcome!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


@app.get("/welcome_token", status_code=200)
def welcome_token(response: Response, token: str, format: str = ""):
    if (token not in app.tokens) or (token == ""):
        raise HTTPException(status_code=401, detail="Unathorised")

    if format == 'json':
        return {"message": "Welcome!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


# 3.4
@app.delete("/logout_session")
def logout_session(session_token: str = Cookie(None), format: str = ""):
    if (session_token not in app.session_tokens) and (session_token not in app.tokens):
        raise HTTPException(status_code=401, detail="Unauthorised")

    if session_token in app.session_tokens:
        app.session_tokens.remove(session_token)
    else:
        app.tokens.remove(session_token)

    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.delete("/logout_token")
def logout_token(token: str, format: str = ""):
    if ((token not in app.tokens) and (token not in app.session_tokens)) or (token == ""):
        raise HTTPException(status_code=401, detail="Unauthorised")

    if token in app.tokens:
        app.tokens.remove(token)
    else:
        app.session_tokens.remove(token)

    return RedirectResponse(url=f"/logged_out?format={format}", status_code=302)


@app.get("/logged_out", status_code=200)
def logged_out(format: str = ""):
    if format == 'json':
        return {"message": "Logged out!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)
