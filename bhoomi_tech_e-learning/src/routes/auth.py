from fastapi import APIRouter, HTTPException, Depends
from database.schemas.auth import UserLogin, Token
from database.repositories.user_repository import UserRepository
from auth import verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=dict)
def login(user_credentials: UserLogin):
    """Login endpoint that returns user info along with token"""
    user = UserRepository.find_by_email(user_credentials.email)
    if not user or not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(hours=8)  # Longer session for admin
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    # Return user info (excluding password) along with token
    user_info = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
        "avatar": user.get("avatar")
    }
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_info
    }
