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
        # Convertir UUID a string antes de guardarlo en MongoDB
        if isinstance(data["customer_id"], uuid.UUID):
            data["customer_id"] = str(data["customer_id"])  

        # Verificar si la notificación ya existe
        if check_notification_exists(data["customer_id"]):
            print(f"⚠️ Notificación ya existe para el customer_id {data['customer_id']}. No se guardará nuevamente.")
            return {"message": "Notificación ya existente, no se guardó duplicado."}

        # Crear la instancia de Notification
        notification = Notification(**data)
        notification_dict = notification.dict()
        notification_dict["customer_id"] = str(notification_dict["customer_id"])  # Asegurar string antes de guardar
        
        # Guardar en MongoDB
        result = collection.insert_one(notification_dict)
        
        return {"_id": str(result.inserted_id), **notification.to_dict()}
    
    except WriteError as e:
        logging.error(f"❌ Error al escribir en MongoDB: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Error al guardar notificación: {e}")
        raise

def check_notification_exists(customer_id):
    """
    Verifica si una notificación ya existe en MongoDB.
    """
    try:
        return collection.find_one({"customer_id": str(customer_id)}) is not None
    except Exception as e:
        logging.error(f"❌ Error al verificar notificación en MongoDB: {e}")
        raise
