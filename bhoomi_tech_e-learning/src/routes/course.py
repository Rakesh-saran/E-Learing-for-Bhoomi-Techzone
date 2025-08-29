from fastapi import APIRouter, HTTPException, Depends
from database.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from database.repositories.course_repository import CourseRepository
from middleware import get_current_user, require_role

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse)
def add_course(course: CourseCreate, current_user = Depends(require_role("instructor"))):
    course_dict = course.dict()
    course_dict["instructor_id"] = str(current_user["_id"])

    result = CourseRepository.create(course_dict)

    # Always return a clean dict, no raw ObjectId
    return {
        "id": str(result.inserted_id),
        "title": course_dict["title"],
        "description": course_dict["description"],
        "instructor_id": course_dict["instructor_id"],
        "lessons": course_dict.get("lessons", []),
        "price": course_dict.get("price"),
        "is_active": course_dict.get("is_active", True)
    }


@router.get("/")
def list_courses():
    courses = CourseRepository.find_all()
    for c in courses:
        c["id"] = str(c["_id"])
        c.pop("_id")
    return courses

@router.get("/{course_id}")
def get_course(course_id: str):
    course = CourseRepository.find_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course["id"] = str(course["_id"])
    course.pop("_id")
    return course

@router.delete("/{course_id}")
def remove_course(course_id: str, current_user = Depends(require_role("instructor"))):
    result = CourseRepository.delete(course_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted"}

@router.put("/{course_id}")
def update_course(course_id: str, course_update: CourseUpdate, current_user = Depends(require_role("instructor"))):
    # Check if course exists
    existing_course = CourseRepository.find_by_id(course_id)
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if current user is the instructor of this course
    if str(existing_course["instructor_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    
    # Prepare update data (only include non-None fields)
    update_data = {}
    if course_update.title is not None:
        update_data["title"] = course_update.title
    if course_update.description is not None:
        update_data["description"] = course_update.description
    if course_update.lessons is not None:
        update_data["lessons"] = course_update.lessons
    if course_update.price is not None:
        update_data["price"] = course_update.price
    if course_update.is_active is not None:
        update_data["is_active"] = course_update.is_active
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    # Update course
    result = CourseRepository.update(course_id, update_data)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Course not found or no changes made")
    
    # Return updated course
    updated_course = CourseRepository.find_by_id(course_id)
    updated_course["id"] = str(updated_course["_id"])
    updated_course.pop("_id")
    return updated_course

@router.get("/instructor/{instructor_id}")
def get_instructor_courses(instructor_id: str):
    courses = CourseRepository.find_by_instructor(instructor_id)
    for c in courses:
        c["id"] = str(c["_id"])
        c.pop("_id")
    return courses
