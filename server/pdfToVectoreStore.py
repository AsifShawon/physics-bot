import os
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


# embedding = OllamaEmbeddings(model="all-minilm:33m")
embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
# embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics_json_nomic")
json_file_path = os.path.join(current_directory, "chunked_physics_data_2.json")

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_documents_from_json(json_data, max_chunk_size=800):
    documents = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_size, chunk_overlap=100)
    for chapter in json_data:
        chapter_name = chapter['chapter']
        title = chapter['title']
        for chunk in chapter['chunks']:
            content = chunk['data']
            split_docs = splitter.split_documents([Document(page_content=content)])
            for doc in split_docs:
                doc.metadata = {
                    "chapter": chapter_name,
                    "title": title,
                    "topic": chunk['topic']
                }
                documents.append(doc)
    return documents

def embed_documents(json_file_path):
    json_data = load_json_data(json_file_path)
    docs = create_documents_from_json(json_data)

    Chroma.from_documents(
        collection_name="physics_db_json",
        embedding=embedding,
        persist_directory=vector_directory,
        documents=docs
    )
    print("Database created")

def db_to_retriever():
    return Chroma(
        collection_name="physics_db_json",
        persist_directory=vector_directory,
        embedding_function=embedding
    )      

def to_unicode(text):
    return text.encode('unicode_escape').decode('ascii')

def search(user_query):
    if not os.path.exists(vector_directory):
        print("Creating database")

        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"{json_file_path} File not found")

        embed_documents(json_file_path)
    else:
        print("Database already exists")
            
    query = to_unicode(user_query)
    db = db_to_retriever()

    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'k': 1, 'score_threshold': 0.5}
    )
    print("query:", query)

    docs = retriever.invoke(query)

    retrieved_docs = ""
    for doc in docs:
        retrieved_docs += f"Chapter: {doc.metadata['chapter']}\n"
        retrieved_docs += f"Title: {doc.metadata['title']}\n"
        retrieved_docs += f"Content: {doc.page_content}\n\n"

    print(retrieved_docs)

    return retrieved_docs

# Example usage
# search("speed of light")
# print(reply)