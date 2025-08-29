import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017/e_learning")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    
config = Config()
