# Admin Panel API Documentation

## Overview
The admin panel provides comprehensive CRUD operations and analytics for managing the Bhoomi Tech E-Learning platform. All admin endpoints require authentication with an admin role.

## Authentication
All admin endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Base URL
All admin endpoints are prefixed with `/admin`

## Endpoints

### 1. Dashboard & Analytics

#### GET `/admin/dashboard`
Get comprehensive admin dashboard statistics including user counts, course counts, enrollments, revenue, growth analytics, and instructor performance.

**Response:**
```json
{
  "stats": {
    "total_users": 150,
    "total_courses": 25,
    "total_enrollments": 300,
    "total_payments": 15000.00,
    "active_users": 140,
    "inactive_users": 10,
    "published_courses": 20,
    "unpublished_courses": 5,
    "new_users_this_week": 12,
    "new_courses_this_week": 3
  },
  "user_growth": [
    {"_id": "2025-09-01", "count": 5},
    {"_id": "2025-09-02", "count": 3}
  ],
  "popular_courses": [
    {
      "_id": {
        "course_id": "course_id_here",
        "course_title": "Python Programming"
      },
      "enrollments": 45
    }
  ],
  "instructor_performance": [
    {
      "instructor_id": "instructor_id",
      "name": "John Doe",
      "email": "john@example.com",
      "total_courses": 5,
      "active_courses": 4,
      "total_enrollments": 120
    }
  ]
}
```

#### GET `/admin/analytics/users`
Get user growth analytics for a specified number of days.

**Query Parameters:**
- `days` (int, default: 30): Number of days to analyze (1-365)

**Response:**
```json
{
  "user_growth": [
    {"_id": "2025-09-01", "count": 5},
    {"_id": "2025-09-02", "count": 3}
  ]
}
```

#### GET `/admin/analytics/courses`
Get course enrollment analytics.

**Query Parameters:**
- `days` (int, default: 30): Number of days to analyze (1-365)

**Response:**
```json
{
  "enrollment_analytics": [
    {
      "_id": {
        "course_id": "course_id",
        "course_title": "Course Title"
      },
      "enrollments": 25
    }
  ]
}
```

#### GET `/admin/analytics/instructors`
Get instructor performance analytics.

**Response:**
```json
{
  "instructor_performance": [
    {
      "instructor_id": "instructor_id",
      "name": "Instructor Name",
      "email": "instructor@email.com",
      "total_courses": 3,
      "active_courses": 2,
      "total_enrollments": 75
    }
  ]
}
```

### 2. User Management

#### GET `/admin/users`
Get all users with pagination and filtering.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20, max: 100): Items per page
- `search` (string, optional): Search in name and email
- `role` (string, optional): Filter by role (admin/instructor/student)
- `is_active` (boolean, optional): Filter by active status

**Response:**
```json
{
  "users": [
    {
      "id": "user_id",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "student",
      "is_active": true,
      "created_at": "2025-09-01T10:00:00Z",
      "last_login": "2025-09-04T08:00:00Z",
      "total_enrollments": 3
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### GET `/admin/users/{user_id}`
Get detailed information about a specific user.

**Response:**
```json
{
  "id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "is_active": true,
  "created_at": "2025-09-01T10:00:00Z",
  "enrollments": 3
}
```

#### POST `/admin/users`
Create a new user.

**Request Body:**
```json
{
  "name": "New User",
  "email": "newuser@example.com",
  "password": "securepassword",
  "role": "student",
  "is_active": true
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": "new_user_id"
}
```

#### PUT `/admin/users/{user_id}`
Update user information.

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com",
  "role": "instructor",
  "is_active": false
}
```

**Response:**
```json
{
  "message": "User updated successfully"
}
```

#### DELETE `/admin/users/{user_id}`
Deactivate a user (soft delete).

**Response:**
```json
{
  "message": "User deactivated successfully"
}
```

#### POST `/admin/users/bulk-action`
Perform bulk actions on multiple users.

**Request Body:**
```json
{
  "action": "activate",
  "ids": ["user_id_1", "user_id_2", "user_id_3"]
}
```

**Actions:** `activate`, `deactivate`, `delete`

**Response:**
```json
{
  "message": "Successfully performed activate on 3 users",
  "affected_count": 3
}
```

### 3. Course Management

#### GET `/admin/courses`
Get all courses with pagination and filtering.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20, max: 100): Items per page
- `search` (string, optional): Search in title and description
- `is_active` (boolean, optional): Filter by active status

**Response:**
```json
{
  "courses": [
    {
      "id": "course_id",
      "title": "Python Programming",
      "description": "Learn Python from basics",
      "instructor_id": "instructor_id",
      "instructor_name": "John Instructor",
      "total_lessons": 10,
      "total_enrollments": 25,
      "price": 99.99,
      "is_active": true,
      "created_at": "2025-09-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 25,
    "pages": 2
  }
}
```

#### GET `/admin/courses/{course_id}`
Get detailed information about a specific course.

**Response:**
```json
{
  "id": "course_id",
  "title": "Python Programming",
  "description": "Learn Python from basics",
  "instructor_id": "instructor_id",
  "instructor_name": "John Instructor",
  "lessons": ["lesson_id_1", "lesson_id_2"],
  "price": 99.99,
  "is_active": true,
  "total_enrollments": 25
}
```

#### POST `/admin/courses`
Create a new course.

**Request Body:**
```json
{
  "title": "New Course",
  "description": "Course description",
  "instructor_id": "instructor_id",
  "lessons": [],
  "price": 149.99,
  "is_active": true
}
```

**Response:**
```json
{
  "message": "Course created successfully",
  "course_id": "new_course_id"
}
```

#### PUT `/admin/courses/{course_id}`
Update course information.

**Request Body:**
```json
{
  "title": "Updated Course Title",
  "description": "Updated description",
  "price": 199.99,
  "is_active": false
}
```

**Response:**
```json
{
  "message": "Course updated successfully"
}
```

#### DELETE `/admin/courses/{course_id}`
Deactivate a course (soft delete).

**Response:**
```json
{
  "message": "Course deactivated successfully"
}
```

#### POST `/admin/courses/bulk-action`
Perform bulk actions on multiple courses.

**Request Body:**
```json
{
  "action": "deactivate",
  "ids": ["course_id_1", "course_id_2"]
}
```

**Actions:** `activate`, `deactivate`, `delete`

**Response:**
```json
{
  "message": "Successfully performed deactivate on 2 courses",
  "affected_count": 2
}
```

### 4. Enrollments Management

#### GET `/admin/enrollments`
Get all enrollments with pagination.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20, max: 100): Items per page

**Response:**
```json
{
  "enrollments": [
    {
      "id": "enrollment_id",
      "user_id": "user_id",
      "user_name": "John Doe",
      "course_id": "course_id",
      "course_title": "Python Programming",
      "enrolled_at": "2025-09-01T10:00:00Z",
      "progress": 75.5
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 300,
    "pages": 15
  }
}
```

### 5. Payments Management

#### GET `/admin/payments`
Get all payments with pagination.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20, max: 100): Items per page

**Response:**
```json
{
  "payments": [
    {
      "id": "payment_id",
      "user_id": "user_id",
      "user_name": "John Doe",
      "amount": 99.99,
      "status": "completed",
      "payment_date": "2025-09-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

### 6. System Management

#### GET `/admin/system/health`
Get system health status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-09-04T12:00:00Z",
  "version": "1.0.0"
}
```

#### GET `/admin/system/stats`
Get detailed system statistics.

**Response:**
```json
{
  "database_stats": {
    "collections": 8,
    "data_size": 1048576,
    "storage_size": 2097152,
    "index_size": 524288
  },
  "collection_stats": {
    "users": 150,
    "courses": 25,
    "enrollments": 300,
    "lessons": 250,
    "payments": 150,
    "reviews": 75,
    "notifications": 500,
    "quizzes": 100
  }
}
```

### 7. Reports

#### GET `/admin/reports/users`
Generate users report.

**Query Parameters:**
- `format` (string, default: json): Report format (json/csv)

**Response:**
```json
{
  "users": [...],
  "total": 150,
  "generated_at": "2025-09-04T12:00:00Z"
}
```

#### GET `/admin/reports/courses`
Generate courses report.

**Query Parameters:**
- `format` (string, default: json): Report format (json/csv)

**Response:**
```json
{
  "courses": [...],
  "total": 25,
  "generated_at": "2025-09-04T12:00:00Z"
}
```

## Error Responses

All endpoints may return the following error responses:

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Data Models

### AdminUserCreate
```json
{
  "name": "string (min 2 chars)",
  "email": "string (valid email)",
  "password": "string (min 6 chars)",
  "role": "admin|instructor|student",
  "is_active": "boolean (default: true)"
}
```

### AdminUserUpdate
```json
{
  "name": "string (optional, min 2 chars)",
  "email": "string (optional, valid email)",
  "role": "admin|instructor|student (optional)",
  "is_active": "boolean (optional)"
}
```

### AdminCourseCreate
```json
{
  "title": "string (min 3 chars)",
  "description": "string (min 10 chars)",
  "instructor_id": "string",
  "lessons": "array of strings (default: [])",
  "price": "number (optional, >= 0)",
  "is_active": "boolean (default: true)"
}
```

### AdminCourseUpdate
```json
{
  "title": "string (optional, min 3 chars)",
  "description": "string (optional, min 10 chars)",
  "instructor_id": "string (optional)",
  "lessons": "array of strings (optional)",
  "price": "number (optional, >= 0)",
  "is_active": "boolean (optional)"
}
```

### BulkAction
```json
{
  "action": "activate|deactivate|delete",
  "ids": "array of strings (min 1 item)"
}
```

## Usage Examples

### Using curl

1. **Get Dashboard:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/admin/dashboard
```

2. **Create User:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"John Doe","email":"john@example.com","password":"password123","role":"student"}' \
     http://localhost:8000/admin/users
```

3. **Search Users:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:8000/admin/users?search=john&role=student&page=1&limit=10"
```

4. **Bulk Activate Users:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"action":"activate","ids":["user_id_1","user_id_2"]}' \
     http://localhost:8000/admin/users/bulk-action
```

## Notes

1. All admin operations require authentication with admin role
2. Soft deletes are used instead of hard deletes to maintain data integrity
3. Pagination is available for all list endpoints
4. Search functionality supports partial matches (case-insensitive)
5. Bulk operations support multiple items for efficiency
6. Analytics data is calculated in real-time from the database
7. System health checks test database connectivity
8. All timestamps are in UTC format
