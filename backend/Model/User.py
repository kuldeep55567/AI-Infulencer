from mongoengine import Document, StringField, EmailField, ListField,DictField
from flask_bcrypt import generate_password_hash, check_password_hash

class User(Document):
    name = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="user")
    queries = ListField(DictField(), default=[])

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
