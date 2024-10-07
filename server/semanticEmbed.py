import os
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import PyPDF2

embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics_semantic_nomic")
pdf_path = os.path.join(current_directory, "Physics.pdf")

def create_chunk(docs):
    chunker = SemanticChunker(embeddings=embeddings, breakpoint_threshold_type="standard_deviation")
    return chunker.create_documents(docs)

def get_pdf_text(path):
    pdf_text = ""
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def check_chunks():
    pdf_text = get_pdf_text(pdf_path)
    chunks = create_chunk([pdf_text])
    return chunks

def store_chunks():
    print('Chunking Started')
    pdf_text = get_pdf_text(pdf_path)
    chunks = create_chunk([pdf_text])
    print('Chunking Finished')
    print('Creating Database')
    Chroma.from_documents(collection_name="physics_db_semantic",embedding=embeddings, persist_directory=vector_directory, documents=chunks)
    print("Database created")

def db_to_retriver():
    return Chroma(
        collection_name="physics_db_semantic",
        persist_directory=vector_directory,
        embedding_function=embeddings
    )

def search(user_query):
    if not os.path.exists(vector_directory):
        print("Creating database")
        store_chunks()
    else:
        print("Database already exists")
            
    query = user_query
    db = db_to_retriver()

    retriver = db.as_retriever(
        # search_type="similarity_score_threshold",
        # search_kwargs={'k':3, 'score_threshold':0.5}
    )
    return retriver.invoke(query)

if __name__ == '__main__':
    response = search('speed of light')
    print(response)
