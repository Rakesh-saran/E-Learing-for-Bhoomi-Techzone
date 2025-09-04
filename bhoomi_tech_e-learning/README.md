# 🎓 Bhoomi Tech E-Learning Platform

A comprehensive FastAPI-based e-learning platform built for Bhoomi Techzone, featuring course management, user authentication, quiz systems, and more.

## 🚀 Features

### 👤 User Management
- **User Registration & Authentication** (Student/Instructor roles)
- **JWT Token-based Security**
- **Profile Management with Avatar Upload**
- **Role-based Access Control**

### 📚 Course Management
- **Course Creation & Management** (Instructor only)
- **Course Updates & Deletion**
- **Course Browsing** (Public access)
- **Instructor Dashboard**

### 📖 Lesson System
- **Lesson Creation & Management**
- **Content Organization by Course**
- **Video & Document Support**

### 🎓 Enrollment System
- **Course Enrollment** (Student)
- **Progress Tracking**
- **My Courses Dashboard**

### ❓ Quiz & Assessment
- **Quiz Creation** (Instructor)
- **Multiple Choice Questions**
- **Quiz Submission & Results**
- **Performance Analytics**

### ⭐ Review & Rating System
- **Course Reviews**
- **Rating System (1-5 stars)**
- **Review Management**

### 🔔 Notification System
- **User Notifications**
- **Read/Unread Status**
- **Notification Management**

### 💳 Payment Integration
- **Payment Processing**
- **Payment History**
- **Transaction Management**

### 📁 File Upload System
- **Avatar Upload**
- **Video Upload**
- **Photo Upload**

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB with PyMongo
- **Authentication**: JWT (JSON Web Tokens)
- **Password Security**: Passlib with bcrypt
- **File Handling**: Python-multipart
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📋 Requirements

```
fastapi
uvicorn[standard]
pymongo
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Rakesh-saran/E-Learing-for-Bhoomi-Techzone.git
cd E-Learing-for-Bhoomi-Techzone
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB
Make sure MongoDB is running on your system or update the connection string in `src/database/__init_db.py`

### 5. Start the Server
```bash
cd src
uvicorn main:app --reload
```

### 6. Access the Application
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📁 Project Structure

```
bhoomi_tech_e-learning/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── auth.py                 # Authentication utilities
│   ├── middleware.py           # Custom middleware
│   ├── config.py              # Configuration settings
│   ├── database/
│   │   ├── __init_db.py       # Database connection
│   │   ├── repositories/      # Data access layer
│   │   └── schemas/          # Pydantic models
│   └── routes/               # API route handlers
├── uploads/                  # User uploaded files
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md               # This file
```

## 🔐 Authentication

The API uses JWT tokens for authentication. After registration/login, include the token in requests:

```
Authorization: Bearer <your_token_here>
```

## 👥 User Roles

### Student
- Register and login
- Browse and enroll in courses
- Take quizzes and track progress
- Leave reviews and ratings
- Manage profile and avatar

### Instructor
- All student capabilities
- Create and manage courses
- Create lessons and quizzes
- View student progress and results
- Manage course content

## 🧪 API Testing

### Postman Collection
Import the provided Postman collection for comprehensive API testing:
- `Bhoomi_ELearning_API_Collection_v2.postman_collection.json`
- `Bhoomi_ELearning_Environment.postman_environment.json`

### Test Coverage
- ✅ 49 API endpoints
- ✅ Complete user workflow testing
- ✅ Role-based permission testing
- ✅ File upload testing
- ✅ Authentication flow testing

## 📊 API Endpoints Overview

### Basic Endpoints
- `GET /` - Welcome message
- `GET /home-feed` - Home feed with courses

### User Management (8 endpoints)
- Registration, login, profile management
- Avatar upload and deletion
- User CRUD operations

### Course Management (6 endpoints)
- Course CRUD operations
- Instructor course management
- Public course browsing

### Lessons (5 endpoints)
- Lesson management and content organization

### Enrollments (4 endpoints)
- Course enrollment and progress tracking

### Quizzes (7 endpoints)
- Quiz creation, submission, and results

### Reviews (4 endpoints)
- Course reviews and rating system

### Notifications (4 endpoints)
- User notification management

### Payments (5 endpoints)
- Payment processing and history

### File Uploads (3 endpoints)
- Avatar, video, and photo uploads

## 🔧 Configuration

### Database Configuration
Update MongoDB connection in `src/database/__init_db.py`:
```python
client = MongoClient("mongodb://localhost:27017/")
db = client["bhoomi_elearning"]
```

### JWT Configuration
Update JWT settings in `src/auth.py`:
```python
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rakesh Saran**
- GitHub: [@Rakesh-saran](https://github.com/Rakesh-saran)
- Project: [E-Learning for Bhoomi Techzone](https://github.com/Rakesh-saran/E-Learing-for-Bhoomi-Techzone)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- MongoDB for the flexible database solution
- Bhoomi Techzone for the project inspiration

## 📞 Support

For support and questions, please open an issue on GitHub or contact the development team.

---

**🎓 Built with ❤️ for Bhoomi Techzone E-Learning Platform**
