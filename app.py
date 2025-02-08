import uvicorn
from fastapi import FastAPI, HTTPException
from model.notification_model import Notification
from repository.repository import save_notification, check_notification_exists
from service.email_service import send_email
import traceback

app = FastAPI()

@app.post("/notify")
def notify_customer(notification: Notification):
    try:
        print("📌 Recibiendo datos:", notification.dict())

        #  Check if the notification already exists in MongoDB
        if check_notification_exists(notification.customer_id):
            print("Notification already sent previously, will not be sent again.")
            return {"message": "The notification has already been sent previously."}

        # Save to MongoDB
        save_notification(notification.dict())

        # Send notification email
        subject = "Bienvenido a nuestro servicio"
        body = f"Hola {notification.name},\n\n{notification.message}\n\nSaludos,\nEquipo de soporte"
        send_email(notification.email, subject, body)

        return {"message": "Notification sent and saved in MongoDB"}

    except Exception as e:
        print("Server error:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint to check if the notification already exists in MongoDB
@app.get("/check_notification")
def check_notification(customer_id: str):
    try:
        exists = check_notification_exists(customer_id)
        return {"exists": exists}
    except Exception as e:
        print("Error verifying notification:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
