# Physics Chatbot

The Physics Chatbot is an interactive, AI-powered educational tool designed to assist users with physics-related questions. It leverages advanced language models and a vector store database to provide accurate and context-aware responses, making it an ideal study companion for students and enthusiasts alike.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Evaluation](#evaluation)
- [Future Work](#future-work)

## Features

- **Interactive Q&A**: Ask physics questions in natural language and receive detailed, human-like answers.
- **Multi-LLM Support**: The chatbot can be configured to use different Large Language Models (LLMs), including local models via Ollama and models from Hugging Face.
- **Vector-Powered Search**: Utilizes ChromaDB to store and retrieve relevant information from physics textbooks, ensuring that answers are accurate and contextually appropriate.
- **Extensible and Modular**: The project is designed with a modular architecture, making it easy to add new data sources, LLMs, or features.

## Project Structure

The project is organized into two main parts: the client and the server. The client-side is responsible for the user interface, while the server handles the backend logic, including the chatbot's core functionality.

Here's a breakdown of the key files and directories:

```
.
├── main.py
├── requirements.txt
└── server/
    ├── chatbot.py
    ├── Embeddings.py
    ├── OllamaLLM.py
    ├── HuggingfaceLLM.py
    ├── pdfProccessing.py
    ├── pdfToVectoreStore.py
    ├── Physics.pdf
    ├── Physics_2.pdf
    ├── db/
    └── Datasets/
```

- **`main.py`**: The entry point for the application, responsible for launching the user interface.
- **`requirements.txt`**: A list of the Python dependencies required for the project.
- **`server/`**: The heart of the application, containing all the backend logic.
  - **`chatbot.py`**: The main chatbot script, which processes user queries and generates responses.
  - **`Embeddings.py`**: Manages the creation of text embeddings for the vector store.
  - **`OllamaLLM.py`**: An interface for using local LLMs with Ollama.
  - **`HuggingfaceLLM.py`**: An interface for using LLMs from the Hugging Face Hub.
  - **`pdfProccessing.py`**: A script for processing PDF files and extracting text.
  - **`pdfToVectoreStore.py`**: A utility for converting PDF content into a vector store.
  - **`Physics.pdf` & `Physics_2.pdf`**: The source materials for the chatbot's knowledge base.
  - **`db/`**: The directory where the ChromaDB vector store is saved.
  - **`Datasets/`**: Contains datasets for evaluating the chatbot's performance.

## Installation

To get started with the Physics Chatbot, you'll need to have Python 3.8 or higher installed on your system. You can then follow these steps to set up the project:

1. **Clone the repository**:

```bash
   git clone [https://github.com/your-username/physics-bot.git](https://github.com/your-username/physics-bot.git)
   cd physics-bot
```

2. **Install the required dependencies**:

```bash
pip install -r requirements.txt
pip install -r server/requirements.txt
```

3. **Set up the vector store**:
  Before you can start using the chatbot, you'll need to create a vector store from the provided PDF files. You can do this by running the following command:
```bash
python server/pdfToVectoreStore.py
```

This will process the `Physics.pdf` and `Physics_2.pdf` files and create a ChromaDB vector store in the `server/db/` directory.

## Usage
Once you've completed the installation, you can run the chatbot by executing the `main.py` script:
```bash
python main.py
```
This will launch a command-line interface where you can start asking physics questions. The chatbot will then use its knowledge base and the configured LLM to provide you with a detailed and accurate answer.

## How It Works
The Physics Chatbot uses a Retrieval-Augmented Generation (RAG) architecture to answer questions. Here's a high-level overview of the process:

1. **User Query**: The user asks a question in natural language.

2. **Vector Search**: The chatbot searches the ChromaDB vector store for relevant information from the physics textbooks.

3. **LLM Prompting**: The retrieved information is then used to create a prompt for the LLM, which is asked to generate a comprehensive answer.

4. **Response Generation**: The LLM processes the prompt and generates a human-like response, which is then displayed to the user.

## Evaluation
The chatbot's performance has been evaluated using a variety of metrics, including BLEU scores and human evaluation. The results of these evaluations can be found in the `server/Datasets/` directory, which contains the datasets used for testing and the corresponding outputs from the chatbot.

## Future Work
The Physics Chatbot is an ongoing project, and there are several areas where it can be improved. Some of the planned future work includes:

* **Improved User Interface**: A graphical user interface (GUI) would make the chatbot more user-friendly and accessible.

* **Support for More Data Sources**: The chatbot could be extended to support other data sources, such as websites, articles, and videos.

* **More Advanced Features**: The chatbot could be enhanced with more advanced features, such as the ability to solve complex physics problems or generate visualizations.
