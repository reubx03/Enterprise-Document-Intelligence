# 🚀 Enterprise Document Intelligence Platform

> A production-grade AI-powered document processing platform that automates OCR, intelligent information extraction, structured data persistence, and enterprise document workflows.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Integrated-4169E1?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![Tesseract OCR](https://img.shields.io/badge/Tesseract-OCR-green)
![Qdrant](https://img.shields.io/badge/Qdrant-Configured-DC244C)
![n8n](https://img.shields.io/badge/n8n-Installed-EA4B71?logo=n8n)
![License](https://img.shields.io/badge/License-MIT-blueviolet)

</p>

---

## 📖 Overview

Enterprise Document Intelligence is a production-oriented backend system designed to automate the complete lifecycle of enterprise document processing.

Instead of manually reviewing invoices, contracts, receipts, purchase orders, resumes, and financial documents, the platform processes uploaded PDFs through an AI-powered pipeline that extracts structured information, validates results, stores them in a relational database, and prepares documents for semantic search and Retrieval-Augmented Generation (RAG).

The project focuses on building production-quality backend architecture rather than only demonstrating AI capabilities. It follows software engineering best practices such as layered architecture, dependency injection, repository pattern, centralized exception handling, schema validation, and RESTful API design.

This project is being developed as a flagship portfolio project to demonstrate practical skills in AI Engineering, Backend Development, Enterprise Software Architecture, and Intelligent Document Processing.

### Project Objectives

- Automate document processing using OCR and Large Language Models (LLMs)
- Extract structured business information from unstructured PDFs
- Persist processed data using PostgreSQL
- Build production-style REST APIs with FastAPI
- Enable semantic document retrieval using vector embeddings
- Implement Retrieval-Augmented Generation (RAG)
- Demonstrate scalable backend architecture suitable for enterprise applications
- Showcase AI engineering best practices in a real-world project

---

## 🚧 Current Project Status

**Current Version:** V1 (Backend Foundation) — 9 of ~22 planned milestones complete

### ✅ Completed

**Infrastructure**
- Docker Desktop & Docker Compose
- PostgreSQL
- Qdrant (installed and running, not yet integrated into the pipeline)
- n8n Community Edition (installed and running, no workflows built yet)
- Local development environment

**Backend Foundation**
- FastAPI project structure with API versioning
- Environment configuration via Pydantic Settings
- Health check API
- Swagger / OpenAPI documentation
- Dependency injection

**OCR Pipeline**
- PDF upload, PDF → image conversion, image preprocessing
- Tesseract OCR integration with per-page confidence scoring
- Structured OCR response models

**AI Extraction Pipeline**
- Google Gemini integration with a document-type-aware prompt builder
- Structured JSON output with per-field confidence scores
- Response parsing and validation
- Pipeline-level exception handling (distinguishes OCR-stage vs. extraction-stage failures)

**Database Layer**
- SQLAlchemy ORM, Alembic migrations, PostgreSQL persistence
- Repository pattern (`DocumentRepository`, `OCRResultRepository`, `ExtractionResultRepository`)

**Document Processing**
- End-to-end OCR → AI extraction pipeline with persistence at each stage
- Document status tracking (`uploaded` → `ocr_complete` → `extraction_complete` / `failed`)
- Document retrieval APIs
- Input validation and error handling

### 🚧 In Progress

- Automated test suite (unit + integration tests for the existing pipeline)
- Vector embeddings and Qdrant integration
- Semantic and hybrid search
- Retrieval-Augmented Generation (RAG)
- Human review workflow
- Dashboard

---

## 🏛 Architecture

The backend follows a layered architecture — each layer has a single responsibility, and no layer reaches past the one directly below it:

```text
API Layer            → handles HTTP requests and responses
     │
Service Layer        → business logic, orchestrates the pipeline
     │
Repository Layer      → encapsulates all database operations
     │
Database              → persistent application data
```

### Processing pipeline

```text
Upload PDF
    │
    ▼
File Validation
    │
    ▼
PDF → Image Conversion  ─┐
    │                    │  OCR Stage (Tesseract)
Image Preprocessing      │  produces per-page text +
    │                    │  confidence scores
Tesseract OCR           ─┘
    │
    ▼
Prompt Building + Google Gemini Extraction
    │  produces structured fields with
    │  per-field confidence scores
    ▼
Response Validation
    │
    ▼
Repository Layer (SQLAlchemy)
    │
    ├──▶ Documents
    ├──▶ OCR Results
    └──▶ Extraction Results
              │
              ▼
        PostgreSQL Database
              │
              ▼
        Document Retrieval APIs
```

**Planned extension (V1 remainder):**

```text
PostgreSQL → Vector Embeddings → Qdrant → Semantic/Hybrid Search → RAG → Human Review UI
```

### Why these technology choices

- **PostgreSQL over SQLite** — supports concurrent writes and JSONB columns for flexible, per-document-type extraction fields without a schema migration for every new document type. SQLite doesn't hold up under the concurrent-access assumptions of a real backend service.
- **Repository pattern over direct ORM calls in routes/services** — `OCRService` and `ExtractionService` have zero knowledge that a database exists; only the repository layer touches a `Session`. This keeps both services independently reusable (e.g., callable from a future batch script or n8n workflow with no database at all) and means a future storage backend change is isolated to the repository implementations.
- **Qdrant over Pinecone/Chroma (planned)** — self-hostable via Docker alongside the rest of the stack, avoiding a managed-API dependency and demonstrating real vector infrastructure rather than just an API key integration.
- **Google Gemini for extraction** — structured JSON output via prompt-enforced schema, chosen for cost and latency during iterative development; the LLM client is isolated behind a thin wrapper (`app/llm/client.py`) specifically so the provider can be swapped without touching the extraction service or API layer.
- **Structured output with per-field confidence over regex-based extraction** — the goal is a system that understands documents contextually, with every extracted value carrying a confidence score that drives human-review routing, not a system that pattern-matches known formats.
- **FastAPI + Pydantic throughout** — schema validation at every layer boundary (request bodies, LLM response parsing, ORM models) rather than trusting data shapes implicitly at any point in the pipeline.

---

## ✨ Features

### Implemented

**Intelligent Document Processing**
- PDF upload with multi-page support
- PDF → image conversion and preprocessing for improved OCR accuracy
- OCR text extraction via Tesseract with per-page confidence scoring

**AI Information Extraction**
- Google Gemini integration with dynamic, document-type-aware prompts
- Structured JSON output with per-field confidence scores
- Document type identified as part of the LLM extraction output (not a separate classification model)
- Response validation and parsing, with malformed-output handling

**Data Persistence**
- PostgreSQL via SQLAlchemy ORM and Alembic migrations
- Repository pattern for all database access
- Document metadata, OCR results, and extraction results stored with full linkage
- Processing status tracked per document, including failure states

**Backend Architecture**
- Layered architecture: API → Service → Repository → Database
- Dependency injection throughout (services and repositories are constructed via FastAPI's DI, not instantiated ad hoc)
- Centralized configuration via Pydantic Settings
- Versioned REST APIs with Swagger/OpenAPI documentation

**Reliability**
- Pipeline-level exception handling that distinguishes which stage failed (OCR vs. extraction) rather than returning generic errors
- Input and file-type validation
- Database consistency on failure (a failed pipeline run is recorded, not silently lost)

### REST APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/upload` | Upload PDF |
| POST | `/api/v1/ocr` | OCR processing |
| POST | `/api/v1/extract` | AI extraction from provided text |
| POST | `/api/v1/documents/process` | Complete OCR → AI extraction → persistence pipeline |
| GET | `/api/v1/documents` | List processed documents (paginated) |
| GET | `/api/v1/documents/{id}` | Retrieve a processed document, its OCR result, and its extraction result |

### In Progress (V1)

- **Semantic search** — vector embeddings, Qdrant integration, similarity retrieval
- **Retrieval-Augmented Generation (RAG)** — context retrieval, question answering, citation-aware responses
- **Human review workflow** — review queue, manual corrections, confidence-based routing, audit trail
- **Dashboard** — processing statistics, confidence metrics, document history, search interface
- **Automated test suite** — unit and integration tests for the pipeline built so far

### Known limitations (current state)

- No automated test suite yet — the pipeline has been manually verified via Swagger against valid PDFs, invalid file types, and corrupted files, but there is no `pytest` coverage in the repo yet.
- Single-document processing only — no batch upload support.
- No retry logic for transient OCR or LLM API failures.
- OCR accuracy is dependent on scan/photo quality; no fallback to an LLM-vision OCR pass yet.
- n8n and Qdrant are running in the local stack but not yet wired into the application.

### Planned (V2)

**Enterprise AI** — multi-document reasoning, AI agents, automated workflow orchestration, document relationship graph

**Enterprise Integrations** — AWS S3, Azure Blob Storage, Google Drive, SharePoint, email ingestion, REST webhooks

**Security** — JWT authentication, RBAC, API keys, audit logging, encryption, secrets management

**Scalability** — Redis caching, background workers (Celery), async processing, batch uploads, Kubernetes deployment

---

## 🛠 Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Backend Framework | FastAPI |
| API Documentation | Swagger / OpenAPI |
| Configuration | Pydantic Settings |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| OCR Engine | Tesseract OCR |
| AI Model | Google Gemini Flash |
| Vector Database | Qdrant (installed, integration in progress) |
| Workflow Automation | n8n Community (installed, no workflows yet) |
| Containerization | Docker & Docker Compose |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
Enterprise-Document-Intelligence/
├── backend/
│   └── app/
│       ├── api/v1/
│       ├── core/
│       ├── db/
│       │   ├── models/
│       │   ├── repositories/
│       │   └── migrations/
│       ├── exceptions/
│       ├── llm/
│       ├── ocr/
│       ├── schemas/
│       ├── services/
│       ├── storage/
│       ├── utils/
│       └── main.py
├── docs/
│   ├── DAILY_LOG.md
│   └── SETUP.md
├── sample_documents/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

| Software | Version |
|---|---|
| Python | 3.12+ |
| Docker Desktop | Latest |
| Git | Latest |
| Tesseract OCR | Latest |
| Poppler | Latest |
| Google Gemini API Key | Required |

### Clone the repository

```bash
git clone https://github.com/reubx03/Enterprise-Document-Intelligence.git
cd Enterprise-Document-Intelligence
```

### Start infrastructure

```bash
docker compose up -d
```

This starts PostgreSQL, Qdrant, and n8n Community Edition. Verify with `docker ps`.

### Backend setup

```bash
cd backend
python -m venv venv
```

Activate the environment:

```bash
# Windows
.\venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file inside `backend/`:

```env
GOOGLE_API_KEY=your_api_key
DATABASE_URL=postgresql://docint:docint@localhost:5432/document_intelligence
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=document_embeddings
```

### Run database migrations

```bash
alembic upgrade head
```

### Run the backend

```bash
uvicorn app.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.

### Available services

| Service | URL |
|---|---|
| FastAPI | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Health Endpoint | http://127.0.0.1:8000/api/v1/health |
| PostgreSQL | localhost:5432 |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| n8n | http://localhost:5678 |

---

## 📄 Example Request / Response

Via Swagger, `POST /api/v1/documents/process` with `invoice.pdf` and `document_type=auto`:

```json
{
  "document_id": "45a4891e-8a0c-4b72-9831-90c1397692dd",
  "document_type": "invoice",
  "fields": {
    "invoice_number": { "value": "INV-1001", "confidence": 0.98 },
    "vendor": { "value": "ABC Pvt Ltd", "confidence": 0.96 }
  },
  "overall_confidence": 0.94,
  "requires_review": false
}
```

---

## 🧪 Testing

Manually verified via Swagger against:

- Valid single- and multi-page PDF processing
- End-to-end OCR → AI extraction → persistence pipeline
- Invalid file type rejection
- Corrupted PDF handling
- Invalid document UUID lookups
- Stage-specific failure handling (OCR failures vs. extraction failures return distinguishable errors)

An automated `pytest` suite covering these scenarios is in progress — see [Known limitations](#known-limitations-current-state). Once added, run it with:

```bash
pytest
```

---

## 📅 Development Roadmap

### V1 — Backend Foundation

**Infrastructure:** ✅ Docker environment · ✅ PostgreSQL · ✅ Qdrant installed · ✅ n8n installed

**Backend:** ✅ FastAPI structure · ✅ API versioning · ✅ Health endpoint · ✅ Swagger docs

**OCR Pipeline:** ✅ Upload · ✅ PDF→image · ✅ Preprocessing · ✅ Tesseract · ✅ Confidence scoring

**AI Extraction:** ✅ Gemini integration · ✅ Prompt builder · ✅ JSON parsing · ✅ Confidence-based schema

**Database Layer:** ✅ SQLAlchemy · ✅ Alembic · ✅ Repository pattern · ✅ Dependency injection

**Processing Pipeline:** ✅ End-to-end pipeline · ✅ Persistence · ✅ Retrieval APIs · ✅ Error handling

**In progress:** ⬜ Automated test suite · ⬜ Vector embeddings · ⬜ Qdrant integration · ⬜ Semantic/hybrid search · ⬜ RAG · ⬜ Human review workflow · ⬜ Dashboard

### V2 — Enterprise Platform

- Multi-document reasoning, AI agents, autonomous workflows, document relationship graph
- JWT authentication, RBAC, audit logging, background workers, Redis caching, batch upload
- AWS S3 / Azure Blob / Google Drive / SharePoint integrations, Kubernetes deployment, CI/CD
- n8n workflow automation (email ingestion, approval workflows, notifications)
- Processing and confidence analytics dashboard

---

## 🎓 Engineering Concepts Demonstrated

**Backend Engineering** — REST API design, layered architecture, dependency injection, repository pattern, service layer pattern, centralized exception handling, configuration management

**Database Engineering** — PostgreSQL, SQLAlchemy ORM, Alembic migrations, relational data modeling with JSONB for flexible schemas

**Artificial Intelligence** — OCR pipelines, prompt engineering, LLM integration, structured output validation, confidence scoring, information extraction

**Enterprise Software Practices** — Docker-based local infrastructure, API documentation, environment/secrets management, production-oriented project structure

---

## 📚 References

Built using FastAPI, SQLAlchemy, PostgreSQL, Alembic, Docker, Tesseract OCR, Google Gemini, Qdrant, and n8n. Official documentation for each is recommended for deeper understanding.

---

## 👨‍💻 Author

Developed by **Reuben Mathew Tharakan** — B.Tech in Artificial Intelligence & Data Science

This repository is a flagship portfolio project demonstrating production-oriented AI backend engineering, intelligent document processing, and enterprise software architecture.

## 📄 License

Released under the MIT License. You are free to learn from, reference, and adapt this code in accordance with the license terms.

## ⭐ Support

If you found this project useful: star the repository, share feedback, open an issue for bugs or suggestions, or follow along as it evolves.

---

<p align="center">

**Built with FastAPI, PostgreSQL, Tesseract OCR, Google Gemini, Docker, and Qdrant.**

</p>
