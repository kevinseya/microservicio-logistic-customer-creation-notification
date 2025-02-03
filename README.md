# microservicio-logistic-customer-creation-notification
# Customer Creation Notification Microservice

This project is a microservice built in Python using **FastAPI** that manages customer creation notifications via email. It is responsible for sending notifications when a new customer is registered in the system.

## 📂 Project Structure

- **`app.py`**: Main entry point of the FastAPI application.
- **`config/config.py`**: Configuration settings for the project.
- **`config/database.py`**: Database connection configuration.
- **`model/notification_model.py`**: Defines the database model for notifications.
- **`repository/repository.py`**: Handles data persistence for notifications.
- **`service/email_service.py`**: Manages email sending functionality.
- **`.env`**: Contains environment variables (not included in Git).
- **`requirements.txt`**: Lists dependencies required for the project.

## 🛠 Requirements

- **Python 3.9** or higher.
- **pip** (Python Package Installer).
- **FastAPI** (for building the API).
- **Uvicorn** (ASGI server for running FastAPI).
- **SQLite/PostgreSQL/MySQL** (Database - configure in `config/database.py`).

## 🚀 Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/kevinseya/microservicio-logistic-customer-creation-notification.git
    ```

2. **Navigate to the project folder**:
    ```bash
    cd microservicio-logistic-customer-creation-notification
    ```

3. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application**:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ```

6. The application will run on: `http://localhost:8000`.

## 📡 Use of API Endpoint

### 1️⃣ **POST /send-notification**

This endpoint sends a notification when a customer is created.

#### 📌 **Request Example**
```http
POST /send-notification
Content-Type: application/json
```
```
{
    "customer_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "phone": "1234567890",
    "message": "Welcome to our service!"
}
```
Response Example
```
{
    "status": "Success",
    "message": "Notification sent successfully"
}
```
Response Codes

  - 200 OK: Notification sent successfully.
  - 400 Bad Request: Missing or invalid parameters.
  - 500 Internal Server Error: Error sending the email.
