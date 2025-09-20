# Sweetshop Project - Running Instructions

This document explains how to run the Sweetshop project (backend and frontend).

---

## Backend

1. Open terminal/command prompt in the backend folder:

```cmd
cd D:\sweetshop\backend
```

2. Create a virtual environment:

```cmd
python -m venv venv
```

3. Activate the virtual environment:

```cmd
venv\Scripts\activate
```

4. Install required dependencies:

```cmd
pip install fastapi uvicorn sqlalchemy aiomysql python-multipart passlib[bcrypt] python-jose[cryptography] pydantic pymysql
```

5. Run the backend server:

```cmd
uvicorn main:app --reload
```

> The backend server should now be running and accessible at `http://127.0.0.1:8000/`.

---

## Frontend

1. Open terminal/command prompt in the frontend folder:

```cmd
cd D:\sweetshop\sweetshop-frontend
```

2. Start the frontend development server:

```cmd
npm start
```

> The frontend application will open in your browser at `http://localhost:3000` (or the port specified in your project).

---

## Notes

- Make sure **Python** (for backend) and **Node.js / npm** (for frontend) are installed on your system.  
- Start the **backend first**, then the frontend.  
- Ensure all dependencies are installed as listed above.
