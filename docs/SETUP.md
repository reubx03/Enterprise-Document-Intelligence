# ⚙️ Enterprise Document Intelligence - Setup Guide

This guide explains how to set up the project for local development.

---

# Prerequisites

Make sure the following are installed:

- Python 3.12+
- Docker Desktop
- Git

---

# Clone Repository

```bash
git clone <repository-url>
cd Enterprise-Document-Intelligence
```

---

# Start Infrastructure

Start all required services:

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- Qdrant
- n8n Community Edition

---

# Backend Setup

Navigate to backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment (Windows):

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

# Available Services

| Service | URL |
|----------|-----|
| FastAPI Docs | http://127.0.0.1:8000/docs |
| Health API | http://127.0.0.1:8000/api/v1/health |
| n8n | http://localhost:5678 |
| PostgreSQL | localhost:5432 |
| Qdrant Dashboard | http://localhost:6333/dashboard |

---

# Stop Development Environment

Infrastructure:

```bash
docker compose down
```

Backend:

Press

```
CTRL + C
```

to stop the FastAPI server.