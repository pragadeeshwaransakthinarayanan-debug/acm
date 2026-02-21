import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:Sai%40123@localhost:5432/erp_db")

# App configuration
APP_NAME = "ERP Backend"
APP_VERSION = "1.0.0"