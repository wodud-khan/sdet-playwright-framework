from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/auth/login")
def login(payload: LoginRequest):
    if payload.email == "test.user@example.com" and payload.password == "password123":
        return {"access_token": "mock-token-abc123"}
    return {"detail": "Invalid credentials"}
