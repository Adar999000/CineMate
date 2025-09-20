import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration - PostgreSQL for Render, SQL Server for local
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    # Fix for newer SQLAlchemy versions
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = DATABASE_URL or "mssql+pyodbc://Adar_SQLLogin_1:sp3bjl1ch2@CinemaDB.mssql.somee.com/CinemaDB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

# Mail settings
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'adar04954@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'ehrf ajby ukoo djsj')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'adar04954@gmail.com')
MAIL_MAX_EMAILS = None
MAIL_ASCII_ATTACHMENTS = False
