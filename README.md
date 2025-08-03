# Physics Chatbot 🔬

The Physics Chatbot is an interactive, AI-powered educational tool designed to assist users with physics-related questions. It leverages advanced language models running locally via Ollama and a vector store database to provide accurate and context-aware responses, making it an ideal study companion for students and enthusiasts alike.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Evaluation](#evaluation)
- [Future Work](#future-work)

## Features

- **Interactive Q&A**: Ask physics questions in natural language and receive detailed, human-like answers through a user-friendly web interface.
- **Local LLM Support**: The chatbot is configured to use local Large Language Models (LLMs) via Ollama, ensuring privacy and control over the model used.
- **Vector-Powered Search**: Utilizes ChromaDB to store and retrieve relevant information from physics textbooks, ensuring that answers are accurate and contextually appropriate.
- **Extensible and Modular**: The project is designed with a modular architecture, making it easy to add new data sources, LLMs, or features.

## Project Structure

The project's core logic and main application are located within the `server/` directory.

```
.
├── server/
│   ├── chatbot.py
│   ├── OllamaLLM.py
│   ├── Embeddings.py
│   ├── pdfToVectoreStore.py
│   ├── Physics.pdf
│   ├── Physics_2.pdf
│   ├── requirements.txt
│   ├── db/
│   └── Datasets/
└── ... (other project files)
```

- **`server/`**: This directory contains the heart of the application.
  - **`chatbot.py`**: The main application script. Running this file with Streamlit launches the web-based chatbot interface.
  - **`OllamaLLM.py`**: An interface for interacting with local LLMs running on Ollama.
  - **`Embeddings.py`**: Manages the creation of text embeddings for the vector store.
  - **`pdfToVectoreStore.py`**: A utility for processing the source PDFs and creating the ChromaDB vector store.
  - **`Physics.pdf` & `Physics_2.pdf`**: The source textbooks for the chatbot's knowledge base.
  - **`requirements.txt`**: A list of the Python dependencies required for the server application.
  - **`db/`**: The default directory where the ChromaDB vector store is saved.
  - **`Datasets/`**: Contains datasets used for evaluating the chatbot's performance.

## Installation

To get started with the Physics Chatbot, you'll need to have Python 3.8 or higher installed. Follow these steps to set up the project:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/physics-bot.git
    cd physics-bot
    ```

2.  **Set up Ollama**:
    The chatbot requires a local LLM to be running via Ollama.
    - Download and install Ollama from [ollama.com](https://ollama.com/).
    - After installation, run Ollama in your terminal.
    - Pull the required model by running the following command:
      ```bash
      ollama run gemma2:2b-instruct-q4_K_M
      ```
    - Keep Ollama running in the background. You can modify the model used in the `server/chatbot.py` file if you have a different model you'd prefer to use.

3.  **Install the required dependencies**:
    Install the necessary Python packages from the root of the project.
    ```bash
    pip install -r requirements.txt
    pip install -r server/requirements.txt
    ```

4.  **Set up the vector store**:
    Before you can start the chatbot, you need to create the vector store from the provided PDF files. Run the following command from the root directory:
    ```bash
    python server/pdfToVectoreStore.py
    ```
    This will process `Physics.pdf` and `Physics_2.pdf`, creating a ChromaDB vector store in the `server/db/` directory.

## Usage

Once you've completed the installation and have Ollama running:

1.  Navigate to the project's root directory in your terminal.
2.  Run the chatbot application using Streamlit:
    ```bash
    streamlit run server/chatbot.py
    ```
This will launch the Physics Chatbot in your web browser, where you can start asking questions.

## How It Works

The Physics Chatbot uses a Retrieval-Augmented Generation (RAG) architecture to answer questions. Here's a high-level overview of the process:

1.  **User Query**: The user asks a question in the Streamlit web interface.
2.  **Vector Search**: The chatbot searches the ChromaDB vector store for relevant information from the physics textbooks.
3.  **LLM Prompting**: The retrieved information is used to create a detailed prompt for the local LLM running on Ollama.
4.  **Response Generation**: The LLM processes the prompt and generates a human-like response, which is then displayed to the user.

## Evaluation

The chatbot's performance has been evaluated using a variety of metrics, including BLEU scores and human evaluation. The results of these evaluations can be found in the `server/Datasets/` directory, which contains the datasets used for testing and the corresponding outputs from the chatbot.

## Future Work

The Physics Chatbot is an ongoing project, and there are several areas where it can be improved. Some of the planned future work includes:

- **Support for More Data Sources**: Extending the chatbot to support other data sources, such as websites, articles, and videos.
- **More Advanced Features**: Enhancing the chatbot with more advanced features, such as the ability to solve complex physics problems or generate visualizations.
- **Fine-tuning Models**: Experimenting with fine-tuning smaller, specialized models for better performance on physics-specific tasks.
