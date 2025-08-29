from fastapi import FastAPI
from src.database.__init_db import client, db
from src.routes.user import router as user_router
from src.routes.course import router as course_router
from src.routes.lesson import router as lesson_router
from src.routes.enrollment import router as enrollment_router
from src.routes.quiz import router as quiz_router
from src.routes.review import router as review_router
from src.routes.notification import router as notification_router
from src.routes.payment import router as payment_router

app = FastAPI(title="Bhoomi Tech E-Learning API", version="1.0.0")

# Include routers
app.include_router(user_router)
app.include_router(course_router)
app.include_router(lesson_router)
app.include_router(enrollment_router)
app.include_router(quiz_router)
app.include_router(review_router)
app.include_router(notification_router)
app.include_router(payment_router)

# Home feed endpoint: returns all courses
from src.database.repositories.course_repository import CourseRepository

@app.get("/home-feed")
def home_feed():
    courses = CourseRepository.find_all()
    for c in courses:
        c["id"] = str(c["_id"])
        c.pop("_id")
    return {"courses": courses}

@app.get("/")
def root():
    return {"message": "Bhoomi Tech E-Learning Backend is running."}
