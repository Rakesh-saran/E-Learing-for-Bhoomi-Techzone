from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from database.schemas.user import UserSchema, UserUpdate
from database.schemas.auth import UserLogin, UserRegister, Token
from database.repositories.user_repository import UserRepository
from auth import verify_password, get_password_hash, create_access_token
from middleware import get_current_user
from datetime import timedelta
import os
import uuid

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=dict)
def register(user: UserRegister):
    if UserRepository.find_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    result = UserRepository.create(user_dict)

    # ✅ MongoDB inserted ID
    user_dict["id"] = str(result.inserted_id)

    # 🚀 Remove MongoDB’s raw ObjectId
    if "_id" in user_dict:
        user_dict.pop("_id")

    # 🚫 Never return password
    user_dict.pop("password")

    return user_dict


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin):
    user = UserRepository.find_by_email(user_credentials.email)
    if not user or not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    current_user["id"] = str(current_user["_id"])
    current_user.pop("_id")
    current_user.pop("password")  # Don't return password
    return current_user

@router.get("/")
def list_users(current_user = Depends(get_current_user)):
    users = UserRepository.find_all()
    for u in users:
        u["id"] = str(u["_id"])
        u.pop("_id")
        u.pop("password")  # Don't return passwords
    return users

@router.get("/{user_id}")
def get_user(user_id: str, current_user = Depends(get_current_user)):
    user = UserRepository.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    user.pop("_id")
    user.pop("password")  # Don't return password
    return user

@router.delete("/{user_id}")
def remove_user(user_id: str, current_user = Depends(get_current_user)):
    result = UserRepository.delete(user_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.put("/{user_id}")
def update_user(user_id: str, user_update: UserUpdate, current_user = Depends(get_current_user)):
    # Check if user exists
    existing_user = UserRepository.find_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only allow users to update their own profile or admin users
    if str(existing_user["_id"]) != str(current_user["_id"]) and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    # Prepare update data (only include non-None fields)
    update_data = {}
    if user_update.name is not None:
        update_data["name"] = user_update.name
    if user_update.email is not None:
        # Check if new email is already taken by another user
        existing_email_user = UserRepository.find_by_email(user_update.email)
        if existing_email_user and str(existing_email_user["_id"]) != user_id:
            raise HTTPException(status_code=400, detail="Email already taken by another user")
        update_data["email"] = user_update.email
    if user_update.avatar is not None:
        update_data["avatar"] = user_update.avatar
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    # Update user
    result = UserRepository.update(user_id, update_data)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or no changes made")
    
    # Return updated user
    updated_user = UserRepository.find_by_id(user_id)
    updated_user["id"] = str(updated_user["_id"])
    updated_user.pop("_id")
    updated_user.pop("password")  # Don't return password
    return updated_user

@router.post("/{user_id}/avatar")
def upload_avatar(user_id: str, avatar: UploadFile = File(...), current_user = Depends(get_current_user)):
    # Check if user exists
    existing_user = UserRepository.find_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only allow users to update their own avatar or admin users
    if str(existing_user["_id"]) != str(current_user["_id"]) and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this user's avatar")
    
    # Validate file type
    if not avatar.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = avatar.filename.split(".")[-1]
    unique_filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = avatar.file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Update user's avatar field
    avatar_url = f"/uploads/avatars/{unique_filename}"
    result = UserRepository.update(user_id, {"avatar": avatar_url})
    
    if result.modified_count == 0:
        # Clean up uploaded file if database update failed
        os.remove(file_path)
        raise HTTPException(status_code=500, detail="Failed to update user avatar")
    
    return {
        "message": "Avatar uploaded successfully",
        "avatar_url": avatar_url,
        "filename": unique_filename
    }

@router.delete("/{user_id}/avatar")
def delete_avatar(user_id: str, current_user = Depends(get_current_user)):
    # Check if user exists
    existing_user = UserRepository.find_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only allow users to delete their own avatar or admin users
    if str(existing_user["_id"]) != str(current_user["_id"]) and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this user's avatar")
    
    # Get current avatar
    current_avatar = existing_user.get("avatar")
    if not current_avatar:
        raise HTTPException(status_code=404, detail="User has no avatar to delete")
    
    # Remove avatar from user record
    result = UserRepository.update(user_id, {"avatar": None})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to remove avatar from user record")
    
    # Try to delete physical file (if it exists)
    if current_avatar.startswith("/uploads/avatars/"):
        file_path = current_avatar.lstrip("/")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # File deletion failed, but we'll still return success since DB was updated
                print(f"Warning: Failed to delete avatar file {file_path}: {str(e)}")
    
    return {"message": "Avatar deleted successfully"}
