# FDM---Diabetes

# Geospatial-Information-Operations

1. Clone the repo
2. Configure the **React frontend**
3. Configure the **FastAPI backend (.venv + requirements.txt)**
4. Run everything locally

---

# 🛠️ Setup Guide (Frontend + Backend)

## 1. Clone the Repository

---

## 2. Backend Setup (FastAPI + PostgreSQL + JWT)

### Prerequisites
- **Python 3.8+**
- **PostgreSQL** installed and running
- **pgAdmin** (optional, for database management)

### Create & Activate Virtual Environment

```bash
cd services
python -m venv .venv
```

Activate the venv:

* **Windows (PowerShell):**

  ```bash
  .venv\Scripts\activate
  ```
* **Mac/Linux:**

  ```bash
  source .venv/bin/activate
  ```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Database Setup

1. **Create PostgreSQL Database:**
   - Open pgAdmin
   - Create a new database named `fdm_diabetes_db` (or your preferred name)

2. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`
   - Update the database URL with your PostgreSQL credentials:
     ```bash
     database_url=postgresql://username:password@localhost:5432/fdm_diabetes_db
     ```
   - Generate a secure JWT secret key:
     ```bash
     py -c "import secrets; print(secrets.token_hex(32))"
     ```
   - Replace the `secret_key` in `.env` with the generated key

3. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

### Run Backend Server

```bash
uvicorn main:app --reload
```

➡ Server will run on [http://localhost:8000](http://localhost:8000)

### Test Authentication Endpoints

Use **Postman** or **curl** to test:

**Signup:**
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","full_name":"Test User"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

**Protected Route (use token from login):**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 3. Frontend Setup (React + Vite)

### Install Node Modules

```bash
cd ../frontend
npm install
```

### Run Frontend Server

```bash
npm run dev
```

➡ Frontend will run on [http://localhost:5173](http://localhost:5173)
