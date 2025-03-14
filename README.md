# Hermes - CheckMK Assistant Chatbot

Hermes is an AI-powered chatbot service designed to help users with questions about CheckMK. It leverages Retrieval-Augmented Generation (RAG) to provide accurate, sourced answers using CheckMK's documentation, blog posts, and integration repositories.

## Features

- **Intelligent Search**: Search through CheckMK documentation, blog posts, and integration repositories with natural language queries
- **Source Attribution**: All responses include source references to the original documents
- **Conversation Memory**: Maintains context throughout the conversation
- **FastAPI Backend**: High-performance web API with health check endpoint
- **Vector Database**: Uses ChromaDB for efficient semantic search capabilities
- **GPT-4o Integration**: Powered by OpenAI's GPT-4o for natural language understanding and generation

## Architecture

The system follows a modern RAG (Retrieval-Augmented Generation) architecture:

1. **Ingestion Pipeline**: Processes documentation, blog posts, and integration data
2. **Vector Database**: Stores embedded documents in separate collections
3. **Search Service**: Retrieves relevant content based on semantic similarity
4. **LLM Agent**: Uses a fine-tuned prompt with GPT-4o to generate helpful responses
5. **API Layer**: Exposes the functionality through a RESTful API

## Installation

### Prerequisites

- Python 3.12+
- OpenAI API key
- ChromaDB

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Tsadoq/check_chatbot.git
   cd check_chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Prepare your data directories:
   ```
   mkdir -p assets/blogposts_samples
   mkdir -p assets/integrations_samples
   mkdir -p assets/docs
   ```

6. Add your CheckMK documentation, blog posts, and integration data to the respective directories.

## Usage

### Data Ingestion

Before starting the service, you need to ingest your data:

```python
from ingestion.ingestor_service import IngestorService

ingestor = IngestorService()
ingestor.ingest_blogposts()
ingestor.ingest_integration()
ingestor.ingest_documentation()
```

### Starting the API Server

Given the nature of this project, that is, a POC, it is suggested to run the API using a single worker. The chat database is not persisted across workers and runs and, as a consequence, using more than one worker might put you in the case where the history of the chat up to a certain point is not accessible to the worker that took your request.

```bash
fastapi run --workers 1 api/app.py  
```

The API will be available at http://0.0.0.0:8000

### API Endpoints
The documentation to the endpoints can be found at  http://0.0.0.0:8000/docs

The following endpoints are available:
- `POST /chat`: Send a message to the chatbot
  ```json
  {
    "message": "How do I configure CheckMK alerts?",
    "chat_id": "unique-session-id"
  }
  ```

- `GET /health_check`: Check if the API is running

## Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key
- Additional configuration can be added to the `.env` file