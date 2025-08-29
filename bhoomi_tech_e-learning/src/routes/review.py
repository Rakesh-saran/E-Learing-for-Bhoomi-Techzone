from fastapi import APIRouter, HTTPException
from database.schemas.review import ReviewSchema
from database.repositories.review_repository import ReviewRepository

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/")
def add_review(review: ReviewSchema):
    result = ReviewRepository.create(review.dict())
    review_dict = review.dict()
    review_dict["id"] = str(result.inserted_id)
    return review_dict

@router.get("/course/{course_id}")
def list_reviews(course_id: str):
    reviews = ReviewRepository.find_by_course(course_id)
    for r in reviews:
        r["id"] = str(r["_id"])
        r.pop("_id")
    return reviews

@router.delete("/{review_id}")
def remove_review(review_id: str):
    result = ReviewRepository.delete(review_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted"}
