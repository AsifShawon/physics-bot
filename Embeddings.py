import PyPDF2
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import Ollama

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=500, overlap=100):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def generate_text(model, text):
    
    # Initialize the Ollama embeddings
    embed = OllamaEmbeddings(model=model)
    pdf_path = 'Thermodynamics.pdf'

    pdf_text = extract_text_from_pdf(pdf_path)
    text_chunks = split_text_into_chunks(pdf_text)

    embeddings = embed.embed_documents(text_chunks)

    vectorStore = InMemoryVectorStore.from_texts(texts=text_chunks, embeddings=embeddings, embedding=embed)

    retriever = vectorStore.as_retriever()
    llm = Ollama(model="gemma2:2b")
    qa_chain = load_qa_chain(llm, chain_type="stuff")
    question = text
    relevant_docs = retriever.get_relevant_documents(question)
    answer = qa_chain.run(input_documents=relevant_docs, question=question)
    print(answer)