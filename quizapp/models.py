from mongoengine import Document, StringField, EmailField, ListField, ReferenceField, DateTimeField, IntField, BooleanField
import hashlib
from datetime import datetime
from mongoengine import Document, StringField, ListField

from mongoengine import (
    Document, StringField, EmailField, ListField, ReferenceField,
    DateTimeField, IntField, BooleanField
)
from datetime import datetime


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(choices=["student", "admin"], default="student")


class Specialization(Document):
    name = StringField(required=True, unique=True)  # software / networking
    description = StringField()


class Book(Document):
    title = StringField(required=True)
    author = StringField()
    specialization = StringField(choices=["software", "networking"])
    file_path = StringField() # مسار الكتاب بعد الرفع
    uploaded_by = StringField()  # user_id
    created_at = DateTimeField(default=datetime.utcnow)


class QuizSession(Document):
    user_id = StringField(required=True)
    specialization = StringField(required=True)
    total_questions = IntField(default=0)
    score = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
