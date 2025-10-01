# Medilocator API

A FastAPI-based backend service for Medilocator, providing chat-based emergency assistance and medical location services.

## Features

- **Chat Interface**: AI-powered chat for emergency assistance
- **User Authentication**: Support for both anonymous and authenticated users
- **Emergency Dispatch**: Automatic emergency service dispatch when needed
- **Location Services**: Integration with location-based services
- **Conversation Logging**: Secure logging of all conversations for emergency response

## Tech Stack

- **Framework**: FastAPI
- **Database**: Postgres, based on Supabase
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Auto-generated with Swagger UI and ReDoc

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mwanjajoel/medilocator-api.git
   cd medilocator-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_API_KEY=your-openai-api-key
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   JWT_SECRET=your-jwt-secret
   ```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Available Endpoints

### Authentication
- `POST /api/v1/auth/anonymous` - Create an anonymous user and get JWT token

### Chat
- `POST /api/v1/chat` - Send a chat message and get AI response

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | API key for OpenAI services | Yes |
| `SUPABASE_URL` | URL for Supabase database | Yes |
| `SUPABASE_KEY` | API key for Supabase | Yes |
| `JWT_SECRET` | Secret key for JWT token generation | Yes |

## Project Structure

```
medilocator-api/
├── app/
│   ├── api/
│   │   ├── routes/         # API route definitions
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── chat.py     # Chat endpoints
│   │   │   └── health.py   # Health check endpoints
│   │   └── __init__.py
│   ├── core/               # Core application configuration
│   │   ├── config.py       # Application settings
│   │   └── security.py     # Security utilities
│   ├── models/             # Database models and schemas
│   ├── services/           # Business logic
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   └── emergency_service.py
│   └── utils/              # Utility functions
├── main.py                 # Application entry point
└── requirements.txt        # Project dependencies
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest
```

## Deployment

[Add deployment instructions here]

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

