from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AdminDashboardStats(BaseModel):
    total_users: int
    total_courses: int
    total_enrollments: int
    total_payments: float
    active_users: int
    inactive_users: int
    published_courses: int
    unpublished_courses: int

class UserManagement(BaseModel):
    id: Optional[str]
    name: str
    email: str
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    total_enrollments: Optional[int] = 0

class CourseManagement(BaseModel):
    id: Optional[str]
    title: str
    description: str
    instructor_id: str
    instructor_name: Optional[str] = None
    total_lessons: int
    total_enrollments: int
    price: Optional[float] = None
    is_active: bool
    created_at: Optional[datetime] = None

class AdminUserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern=r'^(admin|instructor|student)$')
    is_active: bool = True

class AdminUserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    role: Optional[str] = Field(None, pattern=r'^(admin|instructor|student)$')
    is_active: Optional[bool] = None

class AdminCourseCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    instructor_id: str = Field(...)
    price: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=0)
    lessons: List[str] = []
    is_active: bool = True

class AdminCourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=10)
    instructor_id: Optional[str] = None
    lessons: Optional[List[str]] = None
    price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None

class BulkAction(BaseModel):
    action: str = Field(..., pattern=r'^(activate|deactivate|delete)$')
    ids: List[str] = Field(..., min_length=1)

class AdminSearchFilter(BaseModel):
    search_term: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)

class SystemSettings(BaseModel):
    site_name: Optional[str] = None
    maintenance_mode: Optional[bool] = None
    registration_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    max_file_size_mb: Optional[int] = Field(None, ge=1, le=100)
