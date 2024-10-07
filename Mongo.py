from pymongo import MongoClient
from gridfs import GridFS
import schema_def
import os
from dotenv import load_dotenv

load_dotenv() 
class MongoDBHandler:
    def __init__(self, connection_string=os.getenv("MONGO_URI"), database_name="DB_NAME"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name10 = "Expiry Info"
        self.client = None
        self.database = None
        self.files_bucket = None
        self.initialize_mongodb()

    def initialize_mongodb(self):
        self.client = MongoClient(self.connection_string)
        self.database = self.client[self.database_name]
        self.ExpiryCollection = self.database[self.collection_name10]
        self.files_bucket = GridFS(self.database)

    def get_bucket(self):
        return self.files_bucket

    def get_expiry_info_collection(self):
        return self.ExpiryCollection
    
    def shutdown_db_client(self):
        return self.Client.close()

   
