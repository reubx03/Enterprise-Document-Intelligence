# Enterprise Document Intelligence - Local Setup

## Prerequisites

- Docker Desktop
- Git
- VS Code

## Setup

1. Clone the repository

```bash
git clone <repository-url>
```

2. Navigate into the project

```bash
cd Enterprise-Document-Intelligence
```

3. Copy the environment file

```bash
cp .env.example .env
```

(On Windows, simply duplicate `.env.example` and rename it to `.env`.)

4. Start all services

```bash
docker compose up -d
```

## Local Services

| Service | URL |
|----------|-----|
| n8n | http://localhost:5678 |
| PostgreSQL | localhost:5432 |
| Qdrant Dashboard | http://localhost:6333/dashboard |