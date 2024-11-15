from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User data model
class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    height: float


# In-memory storage
users_db: List[User] = []

def log_middleware(request: Request, call_next):
    start_time = time.time()
     # Call the next middleware or route handler
    response = call_next(request)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Request: {request.method} {request.url} | Duration: {duration:.4f} seconds")
    return response


app.middleware("http")(log_middleware)


@app.post("/users", status_code=201)
def create_user(user: User):
    users_db.append(user)
    return {
        "message": "User created successfully",
        "user": user
        }