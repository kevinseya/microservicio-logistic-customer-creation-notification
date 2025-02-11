import uvicorn
from fastapi import FastAPI, HTTPException
from model.notification_model import Notification
from repository.repository import save_notification, check_notification_exists
from service.email_service import send_email
import traceback
from config.config import Config 

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

        # ✅ Enviar correo de notificación
        email_sent = send_email(
    recipient=notification.email,
    subject="🎉 Bienvenido a Nuestro Servicio",
    body=f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 10px;
                    padding: 25px;
                    max-width: 500px;
                    margin: auto;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }}
                h1 {{
                    color: #333;
                    font-size: 22px;
                    margin-bottom: 15px;
                }}
                p {{
                    color: #555;
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 8px 0;
                }}
                .highlight {{
                    color: #007BFF;
                    font-weight: bold;
                }}
                .customer-box {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    margin-top: 15px;
                    text-align: left;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 14px;
                    color: #777;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎉 ¡Bienvenido a Nuestro Servicio! 🎉</h1>
                <p>Hola <strong class="highlight">{notification.name}</strong>,</p>
                <p>Estamos felices de tenerte con nosotros. Aquí tienes un mensaje especial:</p>
                
                <div class="customer-box">
                    <p><strong>📩 Mensaje:</strong> <span class="highlight">{notification.message}</span></p>
                </div>

                <p class="footer">Gracias por confiar en nosotros. ¡Esperamos brindarte la mejor experiencia! 🚀</p>
            </div>
        </body>
    </html>
    """,
    is_html=True  
)

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

PORT = Config.PORT

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
