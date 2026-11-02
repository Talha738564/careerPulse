import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    SESSION_COOKIE_SECURE = os.getenv('COOKIE_SECURE', '0') == '1'
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATA_BACKEND = os.getenv('DATA_BACKEND', 'mock')
    ORACLE_USER = os.getenv('ORACLE_USER')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
    ORACLE_DSN = os.getenv('ORACLE_DSN')
