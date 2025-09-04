#!/usr/bin/env python3
"""
Bhoomi Tech E-Learning Platform - System Check
Verifies all requirements are met to run the platform
"""

import sys
import subprocess
import importlib
import socket
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    try:
        if import_name:
            importlib.import_module(import_name)
        else:
            importlib.import_module(package_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        return False

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 27017))
        sock.close()
        if result == 0:
            print("✅ MongoDB - RUNNING")
            return True
        else:
            print("❌ MongoDB - NOT RUNNING")
            return False
    except Exception as e:
        print(f"❌ MongoDB - ERROR: {e}")
        return False

def check_files():
    """Check if required files exist"""
    base_path = Path(".")
    required_files = [
        "src/main.py",
        "src/auth.py",
        "src/config.py",
        "admin-frontend/index.html",
        "admin-frontend/styles.css",
        "admin-frontend/app.js",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path} - EXISTS")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    print("🎓 Bhoomi Tech E-Learning Platform - System Check")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 0
    
    # Check Python version
    total_checks += 1
    if check_python_version():
        checks_passed += 1
    
    # Check required packages
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pymongo", "pymongo"),
        ("bcrypt", "bcrypt"),
        ("python-jose", "jose"),
        ("python-multipart", "multipart"),
        ("pydantic", "pydantic")
    ]
    
    for package, import_name in required_packages:
        total_checks += 1
        if check_package(package, import_name):
            checks_passed += 1
    
    # Check MongoDB
    total_checks += 1
    if check_mongodb():
        checks_passed += 1
    
    # Check required files
    total_checks += 1
    if check_files():
        checks_passed += 1
    
    print("\n" + "=" * 60)
    print(f"System Check Results: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("\n🎉 All checks passed! Your system is ready to run the platform.")
        print("\nTo start the platform:")
        print("1. Run: start_project.bat")
        print("2. Or manually start: python -m uvicorn src.main:app --reload")
        return True
    else:
        print(f"\n⚠️  {total_checks - checks_passed} issues found. Please fix them before running the platform.")
        print("\nTo fix missing packages, run:")
        print("pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
