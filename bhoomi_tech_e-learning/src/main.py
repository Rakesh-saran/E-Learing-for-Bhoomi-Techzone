from fastapi import FastAPI
from database.__init_db import client, db
from routes.user import router as user_router
from routes.course import router as course_router
from routes.lesson import router as lesson_router
from routes.enrollment import router as enrollment_router
from routes.quiz import router as quiz_router
from routes.review import router as review_router
from routes.notification import router as notification_router
from routes.payment import router as payment_router

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
from database.repositories.course_repository import CourseRepository

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
