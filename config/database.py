from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from config.config import Config 

MONGO_URL = Config.MONGO_URL
MONGO_DB_NAME = Config.MONGO_DB_NAME


def get_database():
    try:
        client = MongoClient(MONGO_URL, 
                           serverSelectionTimeoutMS=5000, 
                           connectTimeoutMS=5000,
                           socketTimeoutMS=5000)
        
        client.admin.command('ismaster')
        
        print("Connection succesfully to MongoDB")
        
        return client[MONGO_DB_NAME]
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        print(f"Error to connect to MongoDBB: {e}")
        raise

db = get_database()