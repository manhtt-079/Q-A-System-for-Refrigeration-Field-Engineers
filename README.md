# Project Name

This project is designed to streamline interactions with text data using advanced NLP techniques and OpenAI's GPT models. It features efficient similarity search with FAISS and offers both console and UI-based interfaces for user interactions.

## Description

The core functionality revolves around processing PDF documents, utilizing OpenAI's embeddings and FAISS for quick information retrieval. It supports natural language queries, providing users with accurate, context-aware responses through both console and UI chat interfaces.

## Installation

### Prerequisites
- Docker
- Docker Compose

### Steps

1. Clone the repository to your local machine.
2. Navigate to the project directory where the `docker-compose.yml` file is located.
3. Replace your-open-api-key to api_key in config.ini
4. Run the following command to build and start the containers in the background:

```shell
docker-compose up -d
```

And navigate to: http://127.0.0.1:8004/docs to interact with bot.


![Sample][./src/pdf_files/Screenshot 2024-06-25 160332.png]
