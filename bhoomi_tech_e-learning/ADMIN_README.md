# Bhoomi Tech E-Learning - Admin Panel Backend

A comprehensive admin panel backend with full CRUD operations for managing users, courses, enrollments, payments, and system analytics.

## Features

### 📊 Dashboard & Analytics
- **Real-time Statistics**: User counts, course counts, enrollments, revenue
- **Growth Analytics**: User growth over time, course enrollment trends
- **Instructor Performance**: Track instructor statistics and performance
- **System Health**: Database connectivity and system status monitoring

### 👥 User Management
- **Complete CRUD Operations**: Create, read, update, delete users
- **Advanced Search & Filtering**: Search by name/email, filter by role/status
- **Bulk Operations**: Activate/deactivate/delete multiple users at once
- **Role Management**: Admin, instructor, student roles
- **Pagination**: Efficient handling of large user datasets

### 📚 Course Management
- **Full Course Lifecycle**: Create, manage, and track courses
- **Instructor Assignment**: Assign and manage course instructors
- **Enrollment Tracking**: Monitor course enrollments and popularity
- **Content Management**: Manage lessons and course structure
- **Price Management**: Set and update course pricing

### 🎓 Enrollment Management
- **Enrollment Tracking**: Monitor all student enrollments
- **Progress Monitoring**: Track student progress across courses
- **Enrollment Analytics**: Analyze enrollment patterns and trends

### 💳 Payment Management
- **Payment Tracking**: Monitor all payment transactions
- **Revenue Analytics**: Track total revenue and payment trends
- **Payment Status**: Monitor payment statuses and failures

### 🔧 System Management
- **Health Monitoring**: Database and system health checks
- **System Statistics**: Database size, collection counts, performance metrics
- **Configuration Management**: System settings and configuration

### 📈 Reports & Analytics
- **User Reports**: Comprehensive user activity and growth reports
- **Course Reports**: Course performance and enrollment reports
- **Custom Analytics**: Detailed analytics with flexible time ranges
- **Export Capabilities**: JSON and CSV export options (planned)

## Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up Environment Variables** (create `.env` file):
```env
MONGO_URL=mongodb://localhost:27017/bhoomi_elearning
SECRET_KEY=your-secret-key-here
```

3. **Set up Admin User**:
```bash
python setup_admin.py
```

4. **Start the Server**:
```bash
python src/main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication
All admin endpoints require authentication. Include the Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Base URL
All admin endpoints are prefixed with `/admin`

### Key Endpoints

#### Dashboard
- `GET /admin/dashboard` - Get comprehensive dashboard data
- `GET /admin/analytics/users` - User growth analytics
- `GET /admin/analytics/courses` - Course enrollment analytics
- `GET /admin/analytics/instructors` - Instructor performance analytics

#### User Management
- `GET /admin/users` - List all users with pagination and filtering
- `GET /admin/users/{user_id}` - Get specific user details
- `POST /admin/users` - Create new user
- `PUT /admin/users/{user_id}` - Update user
- `DELETE /admin/users/{user_id}` - Delete (deactivate) user
- `POST /admin/users/bulk-action` - Bulk operations on users

#### Course Management
- `GET /admin/courses` - List all courses with pagination and filtering
- `GET /admin/courses/{course_id}` - Get specific course details
- `POST /admin/courses` - Create new course
- `PUT /admin/courses/{course_id}` - Update course
- `DELETE /admin/courses/{course_id}` - Delete (deactivate) course
- `POST /admin/courses/bulk-action` - Bulk operations on courses

#### System Management
- `GET /admin/system/health` - System health check
- `GET /admin/system/stats` - Detailed system statistics

#### Reports
- `GET /admin/reports/users` - Generate user reports
- `GET /admin/reports/courses` - Generate course reports

For detailed API documentation, see [ADMIN_API_DOCUMENTATION.md](ADMIN_API_DOCUMENTATION.md)

## Testing

### Automated Testing
Run the comprehensive API test suite:
```bash
python test_admin_api.py
```

This will test:
- Admin authentication
- Dashboard functionality
- User CRUD operations
- Course CRUD operations
- Analytics endpoints
- System health checks
- Bulk operations

### Manual Testing with cURL

1. **Login to get token**:
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bhoomi.com","password":"your_password"}'
```

2. **Get Dashboard**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/admin/dashboard
```

3. **Create User**:
```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123","role":"student"}'
```

### Using Postman
Import the provided Postman collection to test all admin endpoints:
- `Bhoomi_ELearning_API_Collection.postman_collection.json`

## Architecture

### Database Schema
- **Users**: Complete user profiles with roles and status
- **Courses**: Course information with instructor relationships
- **Enrollments**: Student course enrollments with progress tracking
- **Payments**: Payment transactions and status
- **Lessons**: Course content structure
- **Reviews**: Course reviews and ratings
- **Notifications**: System notifications
- **Quizzes**: Course assessments

### Repository Pattern
The system uses a repository pattern for database operations:
- `AdminRepository`: Specialized admin operations and analytics
- `UserRepository`: User CRUD operations
- `CourseRepository`: Course CRUD operations
- `EnrollmentRepository`: Enrollment operations
- `PaymentRepository`: Payment operations

### Authentication & Authorization
- **JWT Tokens**: Secure authentication using JSON Web Tokens
- **Role-based Access**: Admin role required for all admin endpoints
- **Middleware**: Authentication middleware for route protection

## Security Features

1. **Authentication**: JWT-based authentication
2. **Authorization**: Role-based access control
3. **Password Security**: Bcrypt password hashing
4. **Input Validation**: Comprehensive input validation using Pydantic
5. **Soft Deletes**: Maintain data integrity with soft deletes
6. **SQL Injection Protection**: MongoDB with parameterized queries

## Performance Features

1. **Pagination**: Efficient pagination for large datasets
2. **Indexing**: Database indexes for optimal query performance
3. **Bulk Operations**: Efficient bulk operations for multiple records
4. **Caching Strategy**: Ready for caching implementation
5. **Aggregation Pipelines**: Optimized MongoDB aggregation for analytics

## Monitoring & Logging

1. **Health Checks**: Database and system health monitoring
2. **System Statistics**: Comprehensive system metrics
3. **Error Handling**: Comprehensive error handling and responses
4. **API Documentation**: Auto-generated API documentation with FastAPI

## Development

### Project Structure
```
src/
├── database/
│   ├── repositories/
│   │   ├── admin_repository.py      # Admin-specific operations
│   │   ├── user_repository.py       # User CRUD
│   │   ├── course_repository.py     # Course CRUD
│   │   └── ...
│   ├── schemas/
│   │   ├── admin.py                 # Admin API schemas
│   │   ├── user.py                  # User schemas
│   │   └── ...
│   └── __init_db.py                 # Database initialization
├── routes/
│   ├── admin.py                     # Admin routes
│   ├── user.py                      # User routes
│   └── ...
├── auth.py                          # Authentication utilities
├── middleware.py                    # Auth middleware
├── config.py                        # Configuration
└── main.py                          # FastAPI application
```

### Adding New Features

1. **New Endpoints**: Add routes in `src/routes/admin.py`
2. **Database Operations**: Add methods in appropriate repository
3. **Schemas**: Define Pydantic schemas in `src/database/schemas/`
4. **Tests**: Add test cases in `test_admin_api.py`

### Code Quality
- **Type Hints**: Comprehensive type hints throughout
- **Pydantic Models**: Data validation and serialization
- **Error Handling**: Proper HTTP error responses
- **Documentation**: Comprehensive docstrings and comments

## Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
1. **Environment Variables**: Use proper environment configuration
2. **Database**: Use MongoDB Atlas or managed MongoDB service
3. **Security**: Implement HTTPS and proper security headers
4. **Logging**: Implement comprehensive logging
5. **Monitoring**: Add application performance monitoring
6. **Backup**: Implement database backup strategies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Email: support@bhoomitech.com
- Documentation: See ADMIN_API_DOCUMENTATION.md
- Issues: Create GitHub issues for bugs and feature requests

---

**Bhoomi Tech E-Learning Admin Panel** - Empowering education through technology 🎓
