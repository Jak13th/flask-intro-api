import os
from dotenv import load_dotenv


API_KEY= 'YVTbqzJ6vA4YmkcJ9WNP8P5LQRmfS3Wj'
PROPAGATE_EXCEPTIONS = True
# ENVIRONNEMENT CONFIGURATION

## Load .env file
load_dotenv(verbose=True)

## Get these value from .env or from environnement
STRAPI_HOST = os.getenv("STRAPI_HOST", default="localhost:3000")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default="secret-key-123")

## Database config

DEVELOPMENT = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", default="postgresql://postgres:postgres@localhost:5432/postgres")