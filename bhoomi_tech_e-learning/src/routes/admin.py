from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime

# Import schemas
from database.schemas.admin import (
    AdminDashboardStats, UserManagement, CourseManagement,
    AdminUserCreate, AdminUserUpdate, AdminCourseCreate, AdminCourseUpdate,
    BulkAction, AdminSearchFilter, SystemSettings
)
from database.schemas.user import UserSchema, UserUpdate
from database.schemas.course import CourseResponse, CourseCreate, CourseUpdate

# Import repositories
from database.repositories.admin_repository import AdminRepository
from database.repositories.user_repository import UserRepository
from database.repositories.course_repository import CourseRepository
from database.repositories.enrollment_repository import EnrollmentRepository
from database.repositories.payment_repository import PaymentRepository

# Import middleware and auth
from middleware import require_role, get_current_user
from auth import get_password_hash

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

# Simple test endpoint
@router.get("/test")
def test_endpoint():
    """Simple test endpoint"""
    return {"message": "Admin API is working!", "status": "success"}

# ============================================================================
# DASHBOARD AND ANALYTICS
# ============================================================================

@router.get("/dashboard", response_model=Dict[str, Any])
def get_admin_dashboard(current_user = Depends(require_role("admin"))):
    """Get comprehensive admin dashboard statistics"""
    try:
        stats = AdminRepository.get_dashboard_stats()
        
        # Additional analytics
        user_growth = AdminRepository.get_user_growth_analytics(30)
        course_enrollments = AdminRepository.get_course_enrollment_analytics(30)
        instructor_performance = AdminRepository.get_instructor_performance()
        
        return {
            "stats": stats,
            "user_growth": user_growth,
            "popular_courses": course_enrollments,
            "instructor_performance": instructor_performance[:5]  # Top 5 instructors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard data: {str(e)}")

@router.get("/analytics/users")
def get_user_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(require_role("admin"))
):
    """Get user growth analytics"""
    try:
        analytics = AdminRepository.get_user_growth_analytics(days)
        return {"user_growth": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user analytics: {str(e)}")

@router.get("/analytics/courses")
def get_course_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(require_role("admin"))
):
    """Get course enrollment analytics"""
    try:
        analytics = AdminRepository.get_course_enrollment_analytics(days)
        return {"enrollment_analytics": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch course analytics: {str(e)}")

@router.get("/analytics/instructors")
def get_instructor_analytics(current_user = Depends(require_role("admin"))):
    """Get instructor performance analytics"""
    try:
        performance = AdminRepository.get_instructor_performance()
        return {"instructor_performance": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch instructor analytics: {str(e)}")

# ============================================================================
# USER MANAGEMENT
# ============================================================================

@router.get("/users", response_model=Dict[str, Any])
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None, pattern="^(admin|instructor|student)$"),
    is_active: Optional[bool] = Query(None),
    current_user = Depends(require_role("admin"))
):
    """Get all users with pagination and filtering"""
    try:
        skip = (page - 1) * limit
        users = AdminRepository.get_users_with_stats(
            skip=skip, 
            limit=limit, 
            search=search, 
            role_filter=role, 
            active_filter=is_active
        )
        
        # Get total count for pagination
        total_users = UserRepository.find_all()
        total_count = len(total_users)
        
        return {
            "users": users,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.get("/users/{user_id}")
def get_user_details(user_id: str, current_user = Depends(require_role("admin"))):
    """Get detailed user information"""
    try:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert ObjectId to string
        user["id"] = str(user["_id"])
        user.pop("_id")
        
        # Get user enrollments
        enrollments = EnrollmentRepository.find_by_user_id(user_id)
        user["enrollments"] = len(enrollments) if enrollments else 0
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user details: {str(e)}")

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user_data: AdminUserCreate, current_user = Depends(require_role("admin"))):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = UserRepository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Hash password and create user
        user_dict = user_data.dict()
        user_dict["password"] = get_password_hash(user_dict["password"])
        
        user_id = AdminRepository.create_user(user_dict)
        return {"message": "User created successfully", "user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@router.put("/users/{user_id}")
def update_user(
    user_id: str, 
    user_data: AdminUserUpdate, 
    current_user = Depends(require_role("admin"))
):
    """Update user information"""
    try:
        # Check if user exists
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if email is being changed and doesn't conflict
        if user_data.email and user_data.email != user["email"]:
            existing_user = UserRepository.find_by_email(user_data.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")
        
        # Update user
        update_dict = user_data.dict(exclude_unset=True)
        success = AdminRepository.update_user(user_id, update_dict)
        
        if success:
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="No changes were made")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

@router.delete("/users/{user_id}")
def delete_user(user_id: str, current_user = Depends(require_role("admin"))):
    """Delete (deactivate) a user"""
    try:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prevent admin from deleting themselves
        if str(user["_id"]) == str(current_user["_id"]):
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        success = AdminRepository.delete_user(user_id)
        if success:
            return {"message": "User deactivated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to deactivate user")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

@router.post("/users/bulk-action")
def bulk_user_action(action_data: BulkAction, current_user = Depends(require_role("admin"))):
    """Perform bulk actions on users"""
    try:
        # Prevent admin from performing bulk actions on themselves
        current_user_id = str(current_user["_id"])
        if current_user_id in action_data.ids:
            raise HTTPException(status_code=400, detail="Cannot perform bulk actions on your own account")
        
        affected_count = AdminRepository.bulk_user_action(action_data.ids, action_data.action)
        return {
            "message": f"Successfully performed {action_data.action} on {affected_count} users",
            "affected_count": affected_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform bulk action: {str(e)}")

# ============================================================================
# COURSE MANAGEMENT
# ============================================================================

@router.get("/courses")
def get_all_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    """Get all courses with pagination and filtering"""
    try:
        # Simplified version - just return empty list for now to test
        return {
            "courses": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "pages": 0
            }
        }
    except Exception as e:
        print(f"Error fetching courses: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch courses: {str(e)}")

@router.get("/courses/{course_id}")
def get_course_details(course_id: str, current_user = Depends(require_role("admin"))):
    """Get detailed course information"""
    try:
        course = CourseRepository.find_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Convert ObjectId to string and get instructor info
        course["id"] = str(course["_id"])
        course.pop("_id")
        
        # Get instructor details
        instructor = UserRepository.find_by_id(str(course["instructor_id"]))
        course["instructor_name"] = instructor["name"] if instructor else "Unknown"
        course["instructor_id"] = str(course["instructor_id"])
        
        # Get enrollments count
        enrollments = EnrollmentRepository.find_by_course_id(course_id)
        course["total_enrollments"] = len(enrollments) if enrollments else 0
        
        return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch course details: {str(e)}")

@router.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course_data: dict):
    """Create a new course - simplified test version"""
    try:
        print(f"Received course data: {course_data}")  # Debug log
        
        # Basic validation
        required_fields = ['title', 'description']
        for field in required_fields:
            if not course_data.get(field):
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # For testing, just return success without saving to database
        result = {
            "message": "Course created successfully", 
            "course_id": "test_course_123",
            "data": course_data
        }
        
        print(f"Returning result: {result}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Course creation error: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create course: {str(e)}")

@router.put("/courses/{course_id}")
def update_course(
    course_id: str, 
    course_data: AdminCourseUpdate, 
    current_user = Depends(require_role("admin"))
):
    """Update course information"""
    try:
        # Check if course exists
        course = CourseRepository.find_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # If instructor_id is being changed, verify the new instructor
        if course_data.instructor_id:
            instructor = UserRepository.find_by_id(course_data.instructor_id)
            if not instructor:
                raise HTTPException(status_code=400, detail="Instructor not found")
            if instructor["role"] != "instructor":
                raise HTTPException(status_code=400, detail="User must be an instructor")
        
        update_dict = course_data.dict(exclude_unset=True)
        success = AdminRepository.update_course(course_id, update_dict)
        
        if success:
            return {"message": "Course updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="No changes were made")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update course: {str(e)}")

@router.delete("/courses/{course_id}")
def delete_course(course_id: str, current_user = Depends(require_role("admin"))):
    """Delete (deactivate) a course"""
    try:
        course = CourseRepository.find_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        success = AdminRepository.delete_course(course_id)
        if success:
            return {"message": "Course deactivated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to deactivate course")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete course: {str(e)}")

@router.post("/courses/bulk-action")
def bulk_course_action(action_data: BulkAction, current_user = Depends(require_role("admin"))):
    """Perform bulk actions on courses"""
    try:
        affected_count = AdminRepository.bulk_course_action(action_data.ids, action_data.action)
        return {
            "message": f"Successfully performed {action_data.action} on {affected_count} courses",
            "affected_count": affected_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform bulk action: {str(e)}")

# ============================================================================
# ENROLLMENTS AND PAYMENTS MANAGEMENT
# ============================================================================

@router.get("/enrollments")
def get_all_enrollments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_role("admin"))
):
    """Get all enrollments with pagination"""
    try:
        skip = (page - 1) * limit
        
        # This would need to be implemented in EnrollmentRepository
        all_enrollments = EnrollmentRepository.find_all()
        total_count = len(all_enrollments)
        
        # Get paginated enrollments (simplified - you'd want to implement this properly)
        enrollments = all_enrollments[skip:skip+limit]
        
        # Format enrollments with user and course details
        formatted_enrollments = []
        for enrollment in enrollments:
            enrollment["id"] = str(enrollment["_id"])
            enrollment.pop("_id")
            
            # Get user and course details
            user = UserRepository.find_by_id(str(enrollment["user_id"]))
            course = CourseRepository.find_by_id(str(enrollment["course_id"]))
            
            enrollment["user_name"] = user["name"] if user else "Unknown"
            enrollment["course_title"] = course["title"] if course else "Unknown"
            enrollment["user_id"] = str(enrollment["user_id"])
            enrollment["course_id"] = str(enrollment["course_id"])
            
            formatted_enrollments.append(enrollment)
        
        return {
            "enrollments": formatted_enrollments,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch enrollments: {str(e)}")

@router.get("/payments")
def get_all_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_role("admin"))
):
    """Get all payments with pagination"""
    try:
        skip = (page - 1) * limit
        
        # This would need to be implemented in PaymentRepository
        all_payments = PaymentRepository.find_all() if hasattr(PaymentRepository, 'find_all') else []
        total_count = len(all_payments)
        
        payments = all_payments[skip:skip+limit]
        
        # Format payments
        formatted_payments = []
        for payment in payments:
            payment["id"] = str(payment["_id"])
            payment.pop("_id")
            
            # Get user details
            user = UserRepository.find_by_id(str(payment["user_id"]))
            payment["user_name"] = user["name"] if user else "Unknown"
            payment["user_id"] = str(payment["user_id"])
            
            formatted_payments.append(payment)
        
        return {
            "payments": formatted_payments,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch payments: {str(e)}")

# ============================================================================
# SYSTEM MANAGEMENT
# ============================================================================

@router.get("/system/health")
def system_health_check(current_user = Depends(require_role("admin"))):
    """Get system health status"""
    try:
        from database.__init_db import client
        
        # Test database connection
        client.admin.command('ismaster')
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow(),
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }

@router.get("/system/stats")
def get_system_stats(current_user = Depends(require_role("admin"))):
    """Get detailed system statistics"""
    try:
        from database.__init_db import db
        
        # Get database statistics
        db_stats = db.command("dbstats")
        
        return {
            "database_stats": {
                "collections": db_stats.get("collections", 0),
                "data_size": db_stats.get("dataSize", 0),
                "storage_size": db_stats.get("storageSize", 0),
                "index_size": db_stats.get("indexSize", 0)
            },
            "collection_stats": {
                "users": db["users"].estimated_document_count(),
                "courses": db["courses"].estimated_document_count(),
                "enrollments": db["enrollments"].estimated_document_count(),
                "lessons": db["lessons"].estimated_document_count(),
                "payments": db["payments"].estimated_document_count(),
                "reviews": db["reviews"].estimated_document_count(),
                "notifications": db["notifications"].estimated_document_count(),
                "quizzes": db["quizzes"].estimated_document_count()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system stats: {str(e)}")

# ============================================================================
# REPORTS
# ============================================================================

@router.get("/reports/users")
def generate_users_report(
    format: str = Query("json", pattern="^(json|csv)$"),
    current_user = Depends(require_role("admin"))
):
    """Generate users report"""
    try:
        users = AdminRepository.get_users_with_stats(limit=1000)  # Get all users
        
        if format == "json":
            return {"users": users, "total": len(users), "generated_at": datetime.utcnow()}
        else:
            # For CSV, you'd need to implement CSV generation
            raise HTTPException(status_code=501, detail="CSV format not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@router.get("/reports/courses")
def generate_courses_report(
    format: str = Query("json", pattern="^(json|csv)$"),
    current_user = Depends(require_role("admin"))
):
    """Generate courses report"""
    try:
        courses = AdminRepository.get_courses_with_stats(limit=1000)  # Get all courses
        
        if format == "json":
            return {"courses": courses, "total": len(courses), "generated_at": datetime.utcnow()}
        else:
            raise HTTPException(status_code=501, detail="CSV format not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")