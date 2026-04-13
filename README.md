# KWS Backend API

A production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL**.

---

## Project Structure

```
kws_backend/
├── main.py                  # App entry point
├── requirements.txt
├── .env.example             # Copy to .env and fill in your values
│
├── core/
│   ├── config.py            # Settings loaded from .env
│   ├── database.py          # SQLAlchemy engine + session
│   └── security.py          # JWT + password hashing
│
├── models/
│   ├── role.py              # role_master table
│   ├── user.py              # user_master table
│   └── log_transaction.py   # log_transaction table
│
├── schemas/
│   ├── role.py              # Pydantic schemas for Role
│   ├── user.py              # Pydantic schemas for User + Auth
│   └── log_transaction.py   # Pydantic schemas for Logs
│
├── routers/
│   ├── auth.py              # /api/auth/*
│   ├── users.py             # /api/users/*
│   ├── roles.py             # /api/roles/*
│   └── logs.py              # /api/logs/*
│
└── utils/
    └── logger.py            # Helper to write log_transaction rows
```

---

## Setup

### 1. Clone / place the project
```bash
cd kws_backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your MySQL credentials and a strong SECRET_KEY
```

### 5. Make sure MySQL is running and the `kws` database exists
```sql
CREATE DATABASE kws;
```

### 6. Run the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Reference

### 🔐 Auth

| Method | Endpoint         | Auth | Description                  |
|--------|------------------|------|------------------------------|
| POST   | /api/auth/login  | ❌   | Login → returns JWT token    |
| GET    | /api/auth/me     | ✅   | Get current user profile     |

**Login example:**
```json
POST /api/auth/login
{
  "username": "john",
  "password": "secret123"
}
```
Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": 1, "username": "john", ... }
}
```

---

### 👤 Users

| Method | Endpoint          | Auth | Description              |
|--------|-------------------|------|--------------------------|
| POST   | /api/users/       | ❌   | Register new user        |
| GET    | /api/users/       | ✅   | List all users           |
| GET    | /api/users/{id}   | ✅   | Get user by ID           |
| PUT    | /api/users/{id}   | ✅   | Update user              |
| DELETE | /api/users/{id}   | ✅   | Delete user              |

**Register example:**
```json
POST /api/users/
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123",
  "roleid": 1,
  "phone_no": "+971501234567"
}
```

---

### 🏷️ Roles

| Method | Endpoint          | Auth | Description         |
|--------|-------------------|------|---------------------|
| POST   | /api/roles/       | ✅   | Create role         |
| GET    | /api/roles/       | ✅   | List all roles      |
| GET    | /api/roles/{id}   | ✅   | Get role by ID      |
| PUT    | /api/roles/{id}   | ✅   | Update role         |
| DELETE | /api/roles/{id}   | ✅   | Delete role         |

**Create role example:**
```json
POST /api/roles/
{
  "role_name": "Admin"
}
```

---

### 📋 Logs

| Method | Endpoint          | Auth | Description                           |
|--------|-------------------|------|---------------------------------------|
| POST   | /api/logs/        | ✅   | Create log entry manually             |
| GET    | /api/logs/        | ✅   | List logs (filter by user_id, paginate)|
| GET    | /api/logs/{id}    | ✅   | Get single log entry                  |
| DELETE | /api/logs/{id}    | ✅   | Delete one log entry                  |
| DELETE | /api/logs/        | ✅   | Clear ALL log entries                 |

**List logs with filter:**
```
GET /api/logs/?user_id=1&limit=50&offset=0
```

---

## Authentication Flow

1. Register a user via `POST /api/users/`
2. Login via `POST /api/auth/login` → copy the `access_token`
3. In Swagger UI click **Authorize** 🔒 → enter `Bearer <token>`
4. All protected endpoints are now accessible

---

## Notes

- Passwords are hashed with **bcrypt** — never stored in plain text.
- Every create/update/delete action is automatically logged to `log_transaction`.
- Tables are auto-created on startup via SQLAlchemy `create_all`.
- Change `allow_origins=["*"]` in `main.py` to your frontend URL in production.
