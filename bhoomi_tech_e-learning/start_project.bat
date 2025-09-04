@echo off
title Bhoomi Tech E-Learning Platform Launcher
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║             🎓 BHOOMI TECH E-LEARNING PLATFORM 🎓             ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

echo [INFO] Starting Bhoomi Tech E-Learning Platform...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo [INFO] Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

REM Check if MongoDB is available
net start | find /i "MongoDB" >nul
if errorlevel 1 (
    echo [INFO] Starting MongoDB service...
    net start MongoDB >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Could not start MongoDB service automatically
        echo [INFO] Please start MongoDB manually or install MongoDB service
        echo.
    ) else (
        echo [✓] MongoDB service started
        echo.
    )
) else (
    echo [✓] MongoDB service is already running
    echo.
)

REM Change to project directory
cd /d "c:\Users\HP\Desktop\bhoomilearning1\bhoomilearning\bhoomi_tech_e-learning"

echo [INFO] Installing/Checking Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo [✓] Dependencies checked
echo.

echo [INFO] Starting Backend API Server...
echo [INFO] Server will be available at: http://localhost:8000
echo [INFO] API Documentation will be at: http://localhost:8000/docs
echo.

REM Start backend in a new window
start "Bhoomi Backend API" cmd /k "cd /d src && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo [INFO] Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo [INFO] Opening Admin Panel...
start "Bhoomi Admin Panel" "admin-frontend\index.html"

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    🚀 PLATFORM LAUNCHED! 🚀                    ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo [✓] Backend API: http://localhost:8000
echo [✓] API Docs: http://localhost:8000/docs  
echo [✓] Admin Panel: Opened in browser
echo.
echo [INFO] Default Admin Credentials:
echo       Email: admin@bhoomi.com
echo       Password: admin123
echo.
echo [INFO] If admin user doesn't exist, register it first!
echo.
echo Press any key to open additional browser tabs...
pause >nul

echo [INFO] Opening additional resources...
start "API Root" "http://localhost:8000"
start "API Documentation" "http://localhost:8000/docs"

echo.
echo [INFO] All components launched successfully!
echo [INFO] Close this window to keep everything running.
echo [INFO] To stop the backend, close the "Bhoomi Backend API" window.
echo.
pause
