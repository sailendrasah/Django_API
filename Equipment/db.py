import os

from mongoengine import connect, get_db

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/django_api")
MONGODB_DB = os.environ.get("MONGODB_DB", "django_api")

connect(
    alias="default",
    db=MONGODB_DB,
    host=MONGODB_URI,
    serverSelectionTimeoutMS=5000,
)

db = get_db()