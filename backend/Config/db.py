from dotenv import load_dotenv
from mongoengine import connect
import os

load_dotenv()

class Connection:
    def __init__(self):
        self.db = None

    def connect_to_db(self):
        mongo_url = os.getenv("MONGO_URL")
        mongo_name = os.getenv("MONGO_NAME")
        
        self.db = connect(db=mongo_name, host=mongo_url)

    def get_db(self):
        return self.db

    def test_connection(self):
        try:
            self.db.command('ping')
            print("MongoDB connection established successfully.")
        except Exception as e:
            print(f"MongoDB connection failed: {str(e)}")

