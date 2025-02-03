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

        # ✅ Verificar si la notificación ya existe en MongoDB
        if check_notification_exists(notification.customer_id):
            print("⚠️ Notificación ya enviada previamente, no se enviará otra vez.")
            return {"message": "La notificación ya fue enviada previamente."}

        # ✅ Guardar en MongoDB
        save_notification(notification.dict())

        # ✅ Enviar correo de notificación
        subject = "Bienvenido a nuestro servicio"
        body = f"Hola {notification.name},\n\n{notification.message}\n\nSaludos,\nEquipo de soporte"
        send_email(notification.email, subject, body)

        return {"message": "Notificación enviada y guardada en MongoDB"}

    except Exception as e:
        print("❌ Error en el servidor:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Nuevo endpoint para verificar si la notificación ya existe en MongoDB
@app.get("/check_notification")
def check_notification(customer_id: str):
    try:
        exists = check_notification_exists(customer_id)
        return {"exists": exists}
    except Exception as e:
        print("❌ Error al verificar la notificación:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
