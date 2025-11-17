# RAG Graph Wiki Base

A simple LLM chat application built with Python, LangChain, OpenAI, and Neo4j for conversation history storage.

## Features

- 🤖 **Simple LLM Chat**: Interactive chat interface using OpenAI's GPT-3.5-turbo
- 💾 **Conversation Storage**: Store and retrieve chat history using Neo4j graph database
- 🐳 **Docker Support**: Easy Neo4j deployment with Docker Compose
- 📝 **Session Management**: Multiple conversation sessions with persistent history

## Architecture

- **LangChain**: Framework for building LLM applications
- **OpenAI**: GPT-3.5-turbo for natural language understanding and generation
- **Neo4j**: Graph database for storing conversation history and relationships
- **Docker**: Containerized Neo4j deployment

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- OpenAI API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/tunghauvan-interspace/rag-graph-wiki-base.git
cd rag-graph-wiki-base
```

### 2. Set up Python virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
```

### 5. Start Neo4j with Docker

```bash
docker-compose up -d
```

This will start Neo4j on:
- HTTP: http://localhost:7474
- Bolt: bolt://localhost:7687

Default credentials: `neo4j / password123`

## Usage

### Running the Chat Application

```bash
python main.py
```

### Available Commands

Once the application is running, you can use these commands:

- **Regular chat**: Just type your message and press Enter
- `/history` - Display conversation history
- `/clear` - Clear conversation history for current session
- `/exit` - Exit the application

### Example Session

```
============================================================
  RAG Graph Wiki Base - LLM Chat with Neo4j
============================================================
  Commands:
    /history - Show conversation history
    /clear   - Clear conversation history
    /exit    - Exit the application
============================================================

✓ Connected to Neo4j at bolt://localhost:7687
✓ Chat application initialized (Session: session_20250117_153212)
Chat started! Type your message or use commands.

You: What is Python?
Assistant: Python is a high-level, interpreted programming language...

You: /history

--- Conversation History ---
[1] 2025-01-17T15:32:12.123456
You: What is Python?
Assistant: Python is a high-level, interpreted programming language...
--- End of History ---

You: /exit

Goodbye!
```

## Project Structure

```
rag-graph-wiki-base/
├── main.py              # Main entry point
├── chat_app.py          # Chat application logic
├── neo4j_manager.py     # Neo4j database management
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker configuration for Neo4j
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Neo4j Graph Structure

The application creates the following graph structure in Neo4j:

```
(Session)-[:HAS_CONVERSATION]->(Conversation)
```

- **Session Node**: Represents a chat session with a unique ID
- **Conversation Node**: Contains user message, assistant response, and timestamp
- **HAS_CONVERSATION Relationship**: Links sessions to their conversations

## Technology Stack

- **Python 3.8+**: Programming language
- **LangChain 0.3.0**: LLM application framework
- **OpenAI GPT-3.5-turbo**: Large language model
- **Neo4j 5.15.0**: Graph database
- **Docker**: Containerization platform
- **python-dotenv**: Environment variable management

## Troubleshooting

### Neo4j Connection Issues

If you can't connect to Neo4j:

1. Ensure Docker is running: `docker ps`
2. Check if Neo4j container is up: `docker-compose ps`
3. View Neo4j logs: `docker-compose logs neo4j`
4. Restart Neo4j: `docker-compose restart`

### OpenAI API Issues

- Verify your API key is correct in `.env`
- Check your OpenAI account has credits
- Ensure you have internet connectivity

### Module Import Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Development

To stop Neo4j:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
