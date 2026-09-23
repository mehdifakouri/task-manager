# Task Manager

A simple, full-stack management application built from scratch with python and postgres _ without any web framework.

## About

This project demonstrate how a web application works under the hood:

- A custom HTTP server built with python's standard library
- A REST API with full CRUD operations
- postgreSQL database integration
- A frontend in pure HTML, CSS, and JavaScript
- No frameworks - just the fundamentals

The goal was to deeply understand how the web works before jumping into frameworks like Flask and Django.

## Architecture

Browser (5500) → fetch() → Python Server (8000) → SQL → PostgreSQL (5432)

## ✨ Features

- Create, list, complete, and delete tasks
- REST API with proper status codes
- CORS handling
- SQL injection & XSS protection
- Environment variables for credentials

## 🛠️ Tech Stack
```bash
| Layer | Tech |
|---|---|
| Backend | Python 3.13 |
| Server | `http.server` |
| Database | PostgreSQL 15 |
| DB Driver | psycopg 3 |
| Frontend | HTML, CSS, JS |
| Env | python-dotenv |

```


## 📁 Structure

```bashtask-manager-project/
├── backend/
│ ├── db.py # Database connection & CRUD functions
│ └── server.py # HTTP server & API endpoints
├── frontend/
│ ├── index.html # UI structure
│ ├── style.css # Styling
│ └── app.js # Frontend logic & API calls
├── database/
│ └── schema.sql # Database schema
├── .env.example # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```



## 🚀 How to Run

**Prerequisites:** Python 3.13+, PostgreSQL 15+

### 1. Clone & setup

```bash
git clone https://github.com/mehdifakouri/task-manager.git
cd task-manager
python -m venv venv
.\venv\Scripts\Activate.ps1 # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
```

### 2. Database

psql -U postgres

CREATE DATABASE task_manager;
\c task_manager
\i database/schema.sql
\q

### 3. Environment

Copy .env.example → .env, set your password:

DB_PASSWORD=your_password

### 4. Run

Terminal 1 ─ Backend:
python backend/server.py

Terminal 2 ─ Frontend:
cd frontend
python -m http.server 5500

open:http://localhost:5500

### API Endpoints
```bashMethod Endpoint Action
GET /tasks Get all tasks
GET /tasks/{id} Get one task
POST /tasks Create task
PUT /tasks/{id}/complete Mark completed
DELETE /tasks/{id} Delete task
```


### Security

· Parameterized SQL queries
· HTML escaping
· .env for credentials
· CORS headers

### 👤 Author

Mehdi Fakouri — @mehdifakouri
