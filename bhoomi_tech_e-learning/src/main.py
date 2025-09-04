from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Import database connection
try:
    from database.__init_db import client, db
    print("✓ Database connection imported successfully")
except Exception as e:
    print(f"✗ Database connection failed: {e}")

# Import routers with error handling
routers = []

try:
    from routes.auth import router as auth_router
    routers.append(("auth", auth_router))
    print("✓ Auth router imported successfully")
except Exception as e:
    print(f"✗ Auth router failed: {e}")

try:
    from routes.user import router as user_router
    routers.append(("user", user_router))
    print("✓ User router imported successfully")
except Exception as e:
    print(f"✗ User router failed: {e}")

try:
    from routes.course import router as course_router
    routers.append(("course", course_router))
    print("✓ Course router imported successfully")
except Exception as e:
    print(f"✗ Course router failed: {e}")

try:
    from routes.lesson import router as lesson_router
    routers.append(("lesson", lesson_router))
    print("✓ Lesson router imported successfully")
except Exception as e:
    print(f"✗ Lesson router failed: {e}")

try:
    from routes.enrollment import router as enrollment_router
    routers.append(("enrollment", enrollment_router))
    print("✓ Enrollment router imported successfully")
except Exception as e:
    print(f"✗ Enrollment router failed: {e}")

try:
    from routes.quiz import router as quiz_router
    routers.append(("quiz", quiz_router))
    print("✓ Quiz router imported successfully")
except Exception as e:
    print(f"✗ Quiz router failed: {e}")

try:
    from routes.review import router as review_router
    routers.append(("review", review_router))
    print("✓ Review router imported successfully")
except Exception as e:
    print(f"✗ Review router failed: {e}")

try:
    from routes.notification import router as notification_router
    routers.append(("notification", notification_router))
    print("✓ Notification router imported successfully")
except Exception as e:
    print(f"✗ Notification router failed: {e}")

try:
    from routes.payment import router as payment_router
    routers.append(("payment", payment_router))
    print("✓ Payment router imported successfully")
except Exception as e:
    print(f"✗ Payment router failed: {e}")

try:
    from routes.admin import router as admin_router
    routers.append(("admin", admin_router))
    print("✓ Admin router imported successfully")
except Exception as e:
    print(f"✗ Admin router failed: {e}")

print(f"Successfully imported {len(routers)} routers out of 10")

app = FastAPI(title="Bhoomi Tech E-Learning API", version="1.0.0")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001", "*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specify allowed methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files for admin frontend
admin_frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "admin-frontend")
print(f"Admin frontend path: {admin_frontend_path}")
print(f"Path exists: {os.path.exists(admin_frontend_path)}")

if os.path.exists(admin_frontend_path):
    app.mount("/admin-frontend", StaticFiles(directory=admin_frontend_path), name="admin-frontend")
    print("✓ Admin frontend static files mounted")
    
    @app.get("/admin-frontend/", include_in_schema=False)
    async def admin_frontend_index():
        index_path = os.path.join(admin_frontend_path, "index.html")
        print(f"Serving index.html from: {index_path}")
        return FileResponse(index_path)
    
    @app.get("/", include_in_schema=False)
    async def redirect_to_admin():
        return FileResponse(os.path.join(admin_frontend_path, "index.html"))
else:
    print(f"✗ Admin frontend path not found: {admin_frontend_path}")

# Include routers that were successfully imported
for router_name, router in routers:
    try:
        app.include_router(router)
        print(f"✓ {router_name} router registered successfully")
    except Exception as e:
        print(f"✗ {router_name} router registration failed: {e}")

print(f"Total registered routers: {len(routers)}")

# Home feed endpoint: returns all courses
from database.repositories.course_repository import CourseRepository

@app.get("/home-feed")
def home_feed():
    courses = CourseRepository.find_all()
    for c in courses:
        c["id"] = str(c["_id"])
        c.pop("_id")
    return {"courses": courses}

@app.get("/api")
def api_status():
    return {"message": "Bhoomi Tech E-Learning Backend is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
