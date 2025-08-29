from fastapi import APIRouter, HTTPException, Depends
from database.schemas.enrollment import EnrollmentSchema
from database.repositories.enrollment_repository import EnrollmentRepository
from middleware import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

class ProgressUpdate(BaseModel):
    progress: float

@router.post("/")
def enroll(enrollment: EnrollmentSchema, current_user = Depends(get_current_user)):
    # Check if already enrolled
    existing = EnrollmentRepository.find_by_user_and_course(
        str(current_user["_id"]), enrollment.course_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    enrollment_dict = enrollment.dict()
    enrollment_dict["user_id"] = str(current_user["_id"])
    result = EnrollmentRepository.create(enrollment_dict)

    return {
        "id": str(result.inserted_id),
        "user_id": enrollment_dict["user_id"],
        "course_id": enrollment_dict["course_id"],
        "progress": enrollment_dict.get("progress", 0)
    }


@router.get("/")
def list_enrollments(current_user = Depends(get_current_user)):
    enrollments = EnrollmentRepository.find_all()
    for e in enrollments:
        e["id"] = str(e["_id"])
        e.pop("_id")
    return enrollments

@router.get("/my-courses")
def my_courses(current_user = Depends(get_current_user)):
    enrollments = EnrollmentRepository.find_by_user(str(current_user["_id"]))
    for e in enrollments:
        e["id"] = str(e["_id"])
        e.pop("_id")
    return enrollments

@router.put("/{enrollment_id}/progress")
def update_progress(enrollment_id: str, progress_data: ProgressUpdate, current_user = Depends(get_current_user)):
    result = EnrollmentRepository.update_progress(enrollment_id, progress_data.progress)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Progress updated successfully"}

@router.delete("/{enrollment_id}")
def remove_enrollment(enrollment_id: str, current_user = Depends(get_current_user)):
    result = EnrollmentRepository.delete(enrollment_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Enrollment deleted"}
