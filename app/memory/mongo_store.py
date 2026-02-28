# app/memory/mongo_store.py

from pymongo import MongoClient

class MongoConnection:
    """
    Handles ONLY the MongoDB Atlas connection.
    No business logic here.
    """
    def __init__(self, mongo_uri: str, db_name: str = "manusage"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name

        # Create MongoDB client
        self.client = MongoClient(self.mongo_uri)

        # Select database
        self.db = self.client[self.db_name]

    def get_db(self):
        """
        Returns the database object so other modules
        can access collections cleanly.
        """
        return self.db
