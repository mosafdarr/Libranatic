# Libranatic

## Overview

Libranatic is a modern document management system built with FastAPI that processes PDF documents, extracts information, and provides intelligent tagging and search capabilities using LLM technology.

## Features

- PDF document processing and text extraction
- Intelligent document chunking and fact generation using Groq LLM
- Automatic document tagging
- Vector embeddings for semantic search
- PostgreSQL with pgvector for vector storage
- FastAPI-based REST API
- Asynchronous processing
- Modular architecture

## Prerequisites

- Python 3.12+
- PostgreSQL 16+ with pgvector extension
- Poetry for dependency management
- Groq API key for LLM services

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd libranatic
```

2. Install dependencies using Poetry
```bash
poetry install
```

3. Set up environment variables
```bash
cp .env.example .env
```
Configure the following in your `.env`:
- `LLAMA_API_KEY`: Your Groq API key
- `DATABASE_URL`: PostgreSQL connection string
- Other necessary environment variables

4. Set up PostgreSQL with pgvector
```bash
# Install pgvector extension
CREATE EXTENSION vector;
```

5. Run database migrations
```bash
alembic upgrade head
```

## Usage

1. Start the application
```bash
poetry run uvicorn src.index:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `POST /document/upload`: Upload and process PDF documents
- Additional endpoints documentation available in Swagger UI

## Project Structure
src/
├── index.py # Application entry point
├── schema/ # Database models and migrations
├── libintegration/
│ ├── domain/
│ │ ├── apps/ # Application logic
│ │ ├── routers/ # API routes
│ │ └── models/ # Data models
│ └── middlewares/ # Custom middleware
└── settings/ # Configuration


## Development

1. Install development dependencies
```bash
poetry install --with dev
```

2. Run tests
```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[Your chosen license]

## Acknowledgments

- FastAPI
- Groq LLM
- pgvector
- PyPDF2
- sentence-transformers
