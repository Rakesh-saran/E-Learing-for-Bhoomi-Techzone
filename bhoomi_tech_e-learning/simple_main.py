"""
Minimal main.py for the admin panel
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from bson import ObjectId
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MONGO_URL = "mongodb://localhost:27017/e_learning"
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# MongoDB connection
client = MongoClient(MONGO_URL)
db = client.get_database()

app = FastAPI(title="Bhoomi E-Learning Admin API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_active: bool
    created_at: str

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    price: float
    instructor_id: str
    instructor_name: Optional[str] = None
    is_active: bool
    created_at: str

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.users.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def serialize_doc(doc):
    """Convert MongoDB document to serializable dict"""
    if doc:
        if isinstance(doc, dict):
            # Create a copy to avoid modifying original
            doc = doc.copy()
            if "_id" in doc:
                doc["id"] = str(doc["_id"])
                doc.pop("_id", None)
            doc.pop("password", None)  # Remove password from response
            # Convert datetime objects to strings
            for key, value in doc.items():
                if isinstance(value, datetime):
                    doc[key] = value.isoformat()
                elif isinstance(value, ObjectId):
                    doc[key] = str(value)
            return doc
    return None

# Routes
@app.post("/admin/login")
async def admin_login(request: LoginRequest):
    """Admin login"""
    user = db.users.find_one({"email": request.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not verify_password(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admin role required.")
    
    access_token = create_access_token(data={"sub": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": serialize_doc(user)
    }

@app.get("/admin/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    """Get dashboard statistics"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get counts
    total_users = db.users.count_documents({})
    total_courses = db.courses.count_documents({})
    total_enrollments = db.enrollments.count_documents({})
    total_payments = db.payments.count_documents({})
    
    # Get revenue
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    revenue_result = list(db.payments.aggregate(pipeline))
    total_revenue = revenue_result[0]["total"] if revenue_result else 0
    
    # Get recent enrollments
    recent_enrollments = list(db.enrollments.find().sort("enrolled_at", -1).limit(5))
    
    # Add user and course info to enrollments
    processed_enrollments = []
    for enrollment in recent_enrollments:
        user = db.users.find_one({"_id": enrollment["user_id"]})
        course = db.courses.find_one({"_id": enrollment["course_id"]})
        enrollment["user_name"] = user["name"] if user else "Unknown"
        enrollment["course_title"] = course["title"] if course else "Unknown"
        processed_enrollments.append(serialize_doc(enrollment))
    
    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_payments": total_payments,
        "total_revenue": total_revenue,
        "recent_enrollments": processed_enrollments
    }

@app.get("/admin/users")
async def get_users(current_user: dict = Depends(get_current_user)):
    """Get all users"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    users = list(db.users.find().sort("created_at", -1))
    return [serialize_doc(user) for user in users]

@app.post("/admin/users")
async def create_user(user_data: dict, current_user: dict = Depends(get_current_user)):
    """Create a new user"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Hash password
    if "password" in user_data:
        user_data["password"] = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user_data["is_active"] = True
    user_data["created_at"] = datetime.now(timezone.utc)
    user_data["updated_at"] = datetime.now(timezone.utc)
    
    result = db.users.insert_one(user_data)
    
    # Return the created user
    created_user = db.users.find_one({"_id": result.inserted_id})
    return serialize_doc(created_user)

@app.get("/admin/courses")
async def get_courses(current_user: dict = Depends(get_current_user)):
    """Get all courses"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    courses = list(db.courses.find().sort("created_at", -1))
    
    # Add instructor info
    for course in courses:
        if "instructor_id" in course:
            instructor = db.users.find_one({"_id": course["instructor_id"]})
            course["instructor_name"] = instructor["name"] if instructor else "Unknown"
    
    return [serialize_doc(course) for course in courses]

@app.get("/admin/enrollments")
async def get_enrollments(current_user: dict = Depends(get_current_user)):
    """Get all enrollments"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    enrollments = list(db.enrollments.find().sort("enrolled_at", -1))
    
    # Add user and course info
    for enrollment in enrollments:
        user = db.users.find_one({"_id": enrollment["user_id"]})
        course = db.courses.find_one({"_id": enrollment["course_id"]})
        enrollment["user_name"] = user["name"] if user else "Unknown"
        enrollment["course_title"] = course["title"] if course else "Unknown"
    
    return [serialize_doc(enrollment) for enrollment in enrollments]

@app.get("/admin/payments")
async def get_payments(current_user: dict = Depends(get_current_user)):
    """Get all payments"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    payments = list(db.payments.find().sort("created_at", -1))
    
    # Add user and course info
    for payment in payments:
        user = db.users.find_one({"_id": payment["user_id"]})
        course = db.courses.find_one({"_id": payment["course_id"]})
        payment["user_name"] = user["name"] if user else "Unknown"
        payment["course_title"] = course["title"] if course else "Unknown"
    
    return [serialize_doc(payment) for payment in payments]

@app.get("/admin/reviews")
async def get_reviews(current_user: dict = Depends(get_current_user)):
    """Get all reviews"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    reviews = list(db.reviews.find().sort("created_at", -1))
    
    # Add user and course info
    for review in reviews:
        user = db.users.find_one({"_id": review["user_id"]})
        course = db.courses.find_one({"_id": review["course_id"]})
        review["user_name"] = user["name"] if user else "Unknown"
        review["course_title"] = course["title"] if course else "Unknown"
    
    return [serialize_doc(review) for review in reviews]

@app.delete("/admin/reviews/{review_id}")
async def delete_review(review_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a review"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        result = db.reviews.delete_one({"_id": ObjectId(review_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": "Review deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting review {review_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete review")

@app.get("/admin/users/{user_id}")
async def get_user_by_id(user_id: str):
    """Get a specific user by ID"""
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user")

@app.put("/admin/users/{user_id}")
async def update_user(user_id: str, user_data: dict):
    """Update a specific user"""
    try:
        # Hash password if provided
        if "password" in user_data and user_data["password"]:
            user_data["password"] = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())
        elif "password" in user_data:
            del user_data["password"]  # Don't update if empty
        
        user_data["updated_at"] = datetime.utcnow()
        
        result = db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User updated successfully"}
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")

@app.get("/admin/courses/{course_id}")
async def get_course_by_id(course_id: str):
    """Get a specific course by ID"""
    try:
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        course["_id"] = str(course["_id"])
        return course
    except Exception as e:
        logger.error(f"Error getting course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get course")

@app.put("/admin/courses/{course_id}")
async def update_course(course_id: str, course_data: dict):
    """Update a specific course"""
    try:
        course_data["updated_at"] = datetime.utcnow()
        
        result = db.courses.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": course_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return {"message": "Course updated successfully"}
    except Exception as e:
        logger.error(f"Error updating course {course_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update course")

@app.get("/admin/enrollments/{enrollment_id}")
async def get_enrollment_by_id(enrollment_id: str):
    """Get a specific enrollment by ID"""
    try:
        enrollment = db.enrollments.find_one({"_id": ObjectId(enrollment_id)})
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        
        enrollment["_id"] = str(enrollment["_id"])
        return enrollment
    except Exception as e:
        logger.error(f"Error getting enrollment {enrollment_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get enrollment")

@app.delete("/admin/enrollments/{enrollment_id}")
async def delete_enrollment(enrollment_id: str):
    """Delete an enrollment"""
    try:
        result = db.enrollments.delete_one({"_id": ObjectId(enrollment_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        
        return {"message": "Enrollment deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting enrollment {enrollment_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete enrollment")

@app.get("/admin/payments/{payment_id}")
async def get_payment_by_id(payment_id: str):
    """Get a specific payment by ID"""
    try:
        payment = db.payments.find_one({"_id": ObjectId(payment_id)})
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        payment["_id"] = str(payment["_id"])
        return payment
    except Exception as e:
        logger.error(f"Error getting payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get payment")

@app.delete("/admin/payments/{payment_id}")
async def delete_payment(payment_id: str):
    """Delete a payment record"""
    try:
        result = db.payments.delete_one({"_id": ObjectId(payment_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {"message": "Payment deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete payment")

@app.get("/admin/reviews/{review_id}")
async def get_review_by_id(review_id: str):
    """Get a specific review by ID"""
    try:
        review = db.reviews.find_one({"_id": ObjectId(review_id)})
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review["_id"] = str(review["_id"])
        return review
    except Exception as e:
        logger.error(f"Error getting review {review_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get review")

# Analytics Endpoints
@app.get("/admin/analytics/user-growth")
async def get_user_growth():
    """Get user growth analytics"""
    try:
        # Get user registrations by month for the last 6 months
        from datetime import datetime, timedelta
        import calendar
        
        # Calculate the last 6 months
        today = datetime.now()
        months = []
        values = []
        
        for i in range(6):
            month_date = today - timedelta(days=30*i)
            month_name = calendar.month_abbr[month_date.month]
            months.insert(0, month_name)
            
            # Count users created in this month (simulate data for demo)
            # In real implementation, you would query the database
            count = db.users.count_documents({
                "created_at": {
                    "$gte": month_date.replace(day=1),
                    "$lt": (month_date.replace(day=28) + timedelta(days=4)).replace(day=1)
                }
            }) or (10 + i * 15)  # Fallback demo data
            values.insert(0, count)
        
        return {"months": months, "values": values}
    except Exception as e:
        logger.error(f"Error getting user growth: {e}")
        # Return demo data if error
        return {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "values": [10, 25, 40, 68, 95, 120]
        }

@app.get("/admin/analytics/course-popularity")
async def get_course_popularity():
    """Get course popularity analytics"""
    try:
        # Aggregate course enrollment counts
        pipeline = [
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "course_id",
                    "foreignField": "_id",
                    "as": "course"
                }
            },
            {
                "$unwind": "$course"
            },
            {
                "$group": {
                    "_id": "$course.title",
                    "enrollments": {"$sum": 1}
                }
            },
            {
                "$sort": {"enrollments": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        result = list(db.enrollments.aggregate(pipeline))
        courses = [{"name": doc["_id"], "enrollments": doc["enrollments"]} for doc in result]
        
        # If no data, return demo data
        if not courses:
            courses = [
                {"name": "Python Basics", "enrollments": 45},
                {"name": "Web Development", "enrollments": 38},
                {"name": "Data Science", "enrollments": 32},
                {"name": "Mobile Apps", "enrollments": 28}
            ]
        
        return {"courses": courses}
    except Exception as e:
        logger.error(f"Error getting course popularity: {e}")
        return {
            "courses": [
                {"name": "Python Basics", "enrollments": 45},
                {"name": "Web Development", "enrollments": 38},
                {"name": "Data Science", "enrollments": 32},
                {"name": "Mobile Apps", "enrollments": 28}
            ]
        }

@app.get("/admin/analytics/revenue-trends")
async def get_revenue_trends():
    """Get revenue trends analytics"""
    try:
        from datetime import datetime, timedelta
        import calendar
        
        # Calculate revenue for the last 6 months
        today = datetime.now()
        months = []
        revenue = []
        
        for i in range(6):
            month_date = today - timedelta(days=30*i)
            month_name = calendar.month_abbr[month_date.month]
            months.insert(0, month_name)
            
            # Calculate revenue for this month
            month_start = month_date.replace(day=1)
            next_month = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            
            pipeline = [
                {
                    "$match": {
                        "status": "completed",
                        "payment_date": {
                            "$gte": month_start,
                            "$lt": next_month
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total": {"$sum": "$amount"}
                    }
                }
            ]
            
            result = list(db.payments.aggregate(pipeline))
            month_revenue = result[0]["total"] if result else (1200 + i * 400)  # Demo fallback
            revenue.insert(0, int(month_revenue))
        
        return {"months": months, "revenue": revenue}
    except Exception as e:
        logger.error(f"Error getting revenue trends: {e}")
        return {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [1200, 1800, 2400, 3200, 2800, 3600]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/admin/analytics")
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Get analytics data"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # This is a simple analytics endpoint
    # You can expand this with more detailed analytics
    analytics_data = {
        "user_growth": [
            {"month": "Jan", "count": 15},
            {"month": "Feb", "count": 25},
            {"month": "Mar", "count": 35},
            {"month": "Apr", "count": 45},
            {"month": "May", "count": 55},
            {"month": "Jun", "count": 65}
        ],
        "course_enrollment_trends": [
            {"course": "Python Programming", "enrollments": 25},
            {"course": "Web Development", "enrollments": 20},
            {"course": "Data Science", "enrollments": 15},
            {"course": "Mobile Development", "enrollments": 12},
            {"course": "Digital Marketing", "enrollments": 10}
        ],
        "revenue_by_month": [
            {"month": "Jan", "revenue": 1500},
            {"month": "Feb", "revenue": 2200},
            {"month": "Mar", "revenue": 1800},
            {"month": "Apr", "revenue": 2500},
            {"month": "May", "revenue": 3000},
            {"month": "Jun", "revenue": 2800}
        ]
    }
    
    return analytics_data

@app.get("/")
async def root():
    return {"message": "Bhoomi E-Learning Admin API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
