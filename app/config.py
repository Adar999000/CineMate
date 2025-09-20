import os

# Database configuration - PostgreSQL for Render, SQL Server for local
DATABASE_URL = "mssql+pyodbc://Adar_SQLLogin_1:sp3bjl1ch2@CinemaDB.mssql.somee.com/CinemaDB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
# if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    # Fix for newer SQLAlchemy versions
    # DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://Adar_SQLLogin_1:sp3bjl1ch2@CinemaDB.mssql.somee.com/CinemaDB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'supersecretkey'

# Mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'adar04954@gmail.com'  
MAIL_PASSWORD = 'ehrf ajby ukoo djsj'  
MAIL_DEFAULT_SENDER = 'adar04954@gmail.com'
MAIL_MAX_EMAILS = None
MAIL_ASCII_ATTACHMENTS = False
