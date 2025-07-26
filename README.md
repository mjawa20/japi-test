# Japi AI Tutor Backend

A FastAPI-based backend service for Japi's AI-powered English Tutor. It provides conversational onboarding, learning goal setup, and personalized language learning via OpenAI's GPT models.

---

## 🏗️ Architecture Overview

Japi AI Tutor follows a clean, modular, and scalable architecture:

### Layered Breakdown

```
┌────────────────────────────┐
│        Presentation        │
│  - FastAPI Endpoints       │
│  - Request/Response Models │
└────────────────────────────┘
           │
           ▼
┌────────────────────────────┐
│         Services           │
│  - Business Logic          │
│  - Use Cases               │
│  - AI Prompt Management    │
└────────────────────────────┘
           │
           ▼
┌────────────────────────────┐
│        Repository          │
│  - SQLAlchemy ORM          │
│  - Data Persistence        │
└────────────────────────────┘
           │
           ▼
┌────────────────────────────┐
│        Infrastructure      │
│  - Auth / JWT              │
│  - OpenAI GPT API          │
│  - DB Session / Migrations │
└────────────────────────────┘
```

- **Separation of Concerns**: Each layer is responsible for a single purpose.
- **Feature Modules**: All features (e.g., `users`, `chats`) are isolated into folders with their own routes, services, models, and schemas.
- **Dependency Injection**: Via FastAPI's `Depends`.
- **Database Access**: Encapsulated using repository pattern with SQLAlchemy.
- **LLM Integration**: Managed within `infrastructure/ai_service.py`.

---

## 🚀 Features

- 🔐 **Authentication** (JWT-based)
- 💬 **AI Chat Onboarding**
- 📈 **Learning Progress Tracking**
- 📜 **Conversation History**
- 📚 **REST API with OpenAPI Docs**

---

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: PostgreSQL (via SQLAlchemy)
- **AI**: OpenAI GPT
- **Docs**: Swagger & ReDoc
- **Auth**: JWT
- **Deployment**: Docker

---

## 📦 Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API Key

---

## 🧪 Quick Start

```bash
# 1. Clone Repo
git clone https://github.com/yourusername/japi-backend.git
cd japi-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create `.env` file
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/japi_db
SECRET_KEY=your-secret
OPENAI_API_KEY=your-openai-key
```

```bash
# 5. Run server
uvicorn app.main:app --reload
```

---

## 📚 API Endpoints

### 🔐 Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/signup` | POST | Register new user |
| `/users/login` | POST | Authenticate user |
| `/users/me` | GET | Get current user info |

### 💬 Chat
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chats/` | POST | Send message |
| `/chats/` | GET | Get chat history |
| `/chats/` | DELETE | Clear chat history |

---

## 🧩 Project Structure

```
japi-backend/
├── app/
│   ├── config/              # Environment and settings
│   ├── infrastructure/      # DB, AI, Auth
│   ├── modules/
│   │   ├── chats/           # Chat feature (LLM)
│   │   └── users/           # Auth and profile
│   └── shared/              # Dependencies, utils
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## 🔐 AI-Powered Onboarding Flow

1. User sends first message via `/chats/`
2. AI responds with:
   - Personalized greeting
   - Goal-setting prompt
   - Language level assessment
3. Conversation continues with contextual memory

---

## 🔍 OpenAPI Docs

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🐳 Docker (Optional)

```bash
docker build -t japi-backend .
docker run -p 8000:8000 --env-file .env japi-backend
```

---

<div align="center">
  Built with ❤️ by Japi Team
</div>
