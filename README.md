# Japi AI Tutor Backend

A FastAPI-based backend for Japi's AI Tutor, providing a personalized English learning experience through conversational AI.

## 🏗️ Architecture Overview

Japi AI Tutor Backend follows a modular, feature-based architecture with clear separation of concerns:

### Core Components

1. **API Layer** (FastAPI)
   - RESTful endpoints with OpenAPI documentation
   - Request/response validation using Pydantic models
   - JWT-based authentication

2. **Service Layer**
   - Business logic and use cases
   - Handles data validation and processing
   - Manages transactions and error handling

3. **Data Layer**
   - SQLAlchemy ORM for database operations
   - Repository pattern for data access
   - Automatic database migrations

4. **AI Integration**
   - OpenAI GPT for natural language processing
   - Onboarding conversation flow management
   - Response validation and processing

### Key Design Patterns
- **Dependency Injection**: For better testability and loose coupling
- **Repository Pattern**: Abstracts data access logic
- **Service Layer**: Encapsulates business logic
- **Modular Design**: Features separated into independent modules

## 🚀 Features

- **User Authentication** - Secure JWT-based authentication system
- **AI-Powered Chat** - Integration with OpenAI's GPT for natural conversations
- **Onboarding Flow** - Step-by-step setup for new users
- **Conversation History** - Track and retrieve chat history
- **Learning Progress** - Monitor user progress and learning goals
- **RESTful API** - Clean, well-documented endpoints with OpenAPI support

## 🛠 Tech Stack

- **Backend**: Python 3.8+ with FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **AI**: OpenAI GPT Integration
- **API Documentation**: Swagger UI and ReDoc
- **Containerization**: Docker (optional)

## 📦 Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- OpenAI API key
- pip (Python package manager)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/japi-backend.git
   cd japi-backend
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/japi_db
   
   # Authentication
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   
   # OpenAI
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /users/signup` - Register a new user
- `POST /users/login` - Authenticate and get access token
- `GET /users/me` - Get current user details

### Chat
- `POST /chats/` - Send a message (starts onboarding for new users)
- `GET /chats/` - Get chat history
- `DELETE /chats/` - Clear chat history

## 🧩 Project Structure

```
japi-backend/
│
├── app/                     # App logic base folder
│   ├── config/              # App configuration (e.g., env, settings)
│   ├── infrastructure/      # Shared low-level services
│   │   ├── ai_service.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   └── init_db.py
│   ├── modules/             # Feature-based modules
│   │   ├── chats/
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   │   └── services.py
│   │   └── users/
│   │       ├── models.py
│   │       ├── repository.py
│   │       ├── routes.py
│   │       ├── schemas.py
│   │       └── services.py
│   └── shared/              # Shared logic
│       └── deps.py
│
├── venv/                    # Virtual environment (excluded by .gitignore)
├── __pycache__/             # Python bytecode cache (auto-generated)
├── main.py                  # Entry point of FastAPI app
├── .env                     # Local environment variables
├── .env.example             # Example of .env
├── .gitignore               # Git ignore rules
├── requirements.txt         # Project dependencies
└── README.md                # Documentation

```

## 🔍 API Documentation

### Authentication

#### Sign Up
```http
POST /users/signup
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword"
}
```

#### Login
```http
POST /users/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "securepassword"
}
```

### Chat

#### Send Message
```http
POST /chats/
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "Hello, I want to improve my English speaking skills"
}
```

#### Get Chat History
```http
GET /chats/
Authorization: Bearer <token>
```

#### Clear Chat History
```http
DELETE /chats/
Authorization: Bearer <token>
```

<div align="center">
  Made with ❤️ by aman
</div>