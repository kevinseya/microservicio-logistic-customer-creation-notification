from pymongo.errors import WriteError
from config.database import db
from config.config import Config  
from model.notification_model import Notification
import logging
import uuid

MONGO_COLLECTION = Config.MONGO_COLLECTION  
collection = db[MONGO_COLLECTION]

def save_notification(data):
    """
    Guarda la notificación en MongoDB solo si no existe previamente.
    """
    try:
        # Convert UUID to string before saving to MongoDB
        if isinstance(data["customer_id"], uuid.UUID):
            data["customer_id"] = str(data["customer_id"])  

        # Check if the notification already exists
        if check_notification_exists(data["customer_id"]):
            print(f" Notification already exists for customer_id {data['customer_id']}. It will not be saved again.")
            return {"message": "Notification already exists, no duplicate saved."}

        # Create the Notification instance
        notification = Notification(**data)
        notification_dict = notification.dict()
        notification_dict["customer_id"] = str(notification_dict["customer_id"])  # Secure string before saving
        
        # Save to MongoDB
        result = collection.insert_one(notification_dict)
        
        return {"_id": str(result.inserted_id), **notification.to_dict()}
    
    except WriteError as e:
        logging.error(f" Error writing to MongoDB: {e}")
        raise
    except Exception as e:
        logging.error(f" Failed to save notification: {e}")
        raise

def check_notification_exists(customer_id):
    """
    Checks if a notification already exists in MongoDB.
    """
    try:
        return collection.find_one({"customer_id": str(customer_id)}) is not None
    except Exception as e:
        logging.error(f" Error checking notification in MongoDB: {e}")
        raise
