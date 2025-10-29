import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config:
    # Get DATABASE_URL from environment or use local fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgresql://karia:yourpassword@localhost:5432/rentease_db'
)

    # Fix Render's 'postgres://' format
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key')

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')

    # SendGrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
    SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@rentease.com')


# Configure Cloudinary globally
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)
