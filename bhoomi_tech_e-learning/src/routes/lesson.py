from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from database.schemas.lesson import LessonSchema
from database.repositories.lesson_repository import LessonRepository
from middleware import get_current_user, require_role
import os
import shutil

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.post("/")
def add_lesson(lesson: LessonSchema, current_user = Depends(require_role("instructor"))):
    result = LessonRepository.create(lesson.dict())
    lesson_dict = lesson.dict()
    lesson_dict["id"] = str(result.inserted_id)
    return lesson_dict

@router.post("/{lesson_id}/upload-video")
async def upload_video(lesson_id: str, file: UploadFile = File(...), current_user = Depends(require_role("instructor"))):
    # Create uploads directory if it doesn't exist
    upload_dir = "../uploads/videos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = f"{upload_dir}/{lesson_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update lesson with video URL
    lesson = LessonRepository.find_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Update video_url in database (you'll need to add an update method to repository)
    return {"message": "Video uploaded successfully", "file_path": file_path}

@router.get("/")
def list_lessons():
    lessons = LessonRepository.find_all()
    for l in lessons:
        l["id"] = str(l["_id"])
        l.pop("_id")
    return lessons

@router.get("/{lesson_id}")
def get_lesson(lesson_id: str):
    lesson = LessonRepository.find_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    lesson["id"] = str(lesson["_id"])
    lesson.pop("_id")
    return lesson

@router.delete("/{lesson_id}")
def remove_lesson(lesson_id: str, current_user = Depends(require_role("instructor"))):
    result = LessonRepository.delete(lesson_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"message": "Lesson deleted"}
