import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import PyPDF2

# embedding = OllamaEmbeddings(model="all-minilm:33m")
embedding = OllamaEmbeddings(model="nomic-embed-text:latest")
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics_recursive_nomic")
file_path = os.path.join(current_directory, "Physics.pdf")

def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def split_text_into_chunks(texts, chunk_size=1000, overlap=100):
    # splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    documents = [Document(page_content=texts)]
    return splitter.split_documents(documents)

def embed_documents(pdf_path):

    pdf_documents = extract_text_from_pdf(pdf_path)
    docs = split_text_into_chunks(pdf_documents)

    Chroma.from_documents(collection_name="physics_db_recursive",embedding=embedding, persist_directory=vector_directory, documents=docs)
    print("Database created")


def db_to_retriver():
    return Chroma(
        collection_name="physics_db_recursive",
        persist_directory=vector_directory,
        embedding_function=embedding
    )      

def search(user_query):
    if not os.path.exists(vector_directory):
        print("Creating database")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} File not found")

        embed_documents(file_path)
    else:
        print("Database already exists")
            
    query = user_query
    db = db_to_retriver()

    retriver = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'k':3, 'score_threshold':0.5}
    )
    print("query:", query)

    docs = retriver.invoke(query)

    retrived_docs = ""
    for doc in docs:
        retrived_docs += doc.page_content +"\n"

    print(retrived_docs)

    return retrived_docs
# search("The uses of computer?")