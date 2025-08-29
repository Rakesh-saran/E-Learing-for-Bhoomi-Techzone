from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None
