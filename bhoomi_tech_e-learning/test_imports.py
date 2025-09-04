#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

# Test each route import individually
route_modules = [
    'routes.auth',
    'routes.user', 
    'routes.course',
    'routes.lesson',
    'routes.enrollment',
    'routes.quiz',
    'routes.review',
    'routes.notification',
    'routes.payment',
    'routes.admin'
]

print("Testing route imports...")

for module in route_modules:
    try:
        __import__(module)
        print(f"✓ {module} - OK")
    except Exception as e:
        print(f"✗ {module} - ERROR: {e}")

print("\nTesting main app creation...")
try:
    from main import app
    print("✓ Main app created successfully")
    print(f"✓ App routes: {len(app.routes)} routes registered")
except Exception as e:
    print(f"✗ Main app creation failed: {e}")
