#!/usr/bin/env python3

import uvicorn
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static files for admin frontend
admin_frontend_path = os.path.join(os.path.dirname(__file__), "admin-frontend")
if os.path.exists(admin_frontend_path):
    app.mount("/admin-frontend", StaticFiles(directory=admin_frontend_path), name="admin-frontend")
    
    @app.get("/admin-frontend/", include_in_schema=False)
    async def admin_frontend_index():
        return FileResponse(os.path.join(admin_frontend_path, "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
