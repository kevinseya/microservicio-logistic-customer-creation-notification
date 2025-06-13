from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class Notification(BaseModel):
    customer_id: UUID
    name: str
    lastname: str
    email: EmailStr
    message: Optional[str] = "Bienvenido a Logistic y Delivery ✨"
    date: datetime = datetime.utcnow()

    def to_dict(self):
        return {
            "customer_id": str(self.customer_id),
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "message": self.message,
            "date": self.date.isoformat()
        }
