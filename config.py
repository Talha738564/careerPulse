import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATA_BACKEND = os.getenv('DATA_BACKEND', 'mock')
    ORACLE_USER = os.getenv('ORACLE_USER')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
    ORACLE_DSN = os.getenv('ORACLE_DSN')
