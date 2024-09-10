import PyPDF2
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

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

    template = """
    You are a Physics bot and answer only physics questions and in English.
    If there is no exact answer,don't reply with partial answer. and ask user physics related question.
    Answer based on this RAG content: {rag_content} and jsut simmillar to this.
    Question: {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["rag_content", "question"])

    # Retrieve relevant chunks
    question = text
    relevant_docs = retriever.invoke(question)

    # Combine the relevant document content
    rag_content = "\n".join([doc.page_content for doc in relevant_docs])

    # Create the input for the chain
    chain_input = {"rag_content": rag_content, "question": question}

    # Create the chain and invoke it
    chain = prompt | llm
    answer = chain.invoke(chain_input)

    print(answer)
    return answer

# generate_text("gemma2:2b", "What is the formula for the force of gravity?")