from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search

# Initialize chat history and system message
chatHistory = []
systemMessage = """You are a helpful physics assistant. 
Always try to provide examples directly from the physics book. 
Your topics are []
If the answer is not found in the documents, respond with 'I'm not sure'. 
Do not answer questions unrelated to physics."""

chatHistory.append(SystemMessage(content=systemMessage))

# Initialize model once
# "llama3.2:3b", "gemma2:9b", "gemma2:2b", "qwen2.5:3b"
ollama_model = Ollama(model="gemma2:2b")
# ollama_model = Ollama(model="qwen2.5:3b")

def generate_text(query):
    # Retrieve context from physics documents
    retrieved_text = search(query)

    # Check if relevant content was found
    if retrieved_text != "No relevant docs were retrieved using the relevance score threshold 0.5":
        # Modify the context to request specific examples from the retrieved documents
        context = (f"Here are some documents that might help answer the question: \n{retrieved_text}\n"
                   f"Please provide an example from the book related to the question: {query}. "
                   f"Only use information from the provided documents. If no example is available in the documents, respond with 'I'm not sure'.")
    else:
        context = f"The question is: {query}. Unfortunately, I couldn't find any relevant documents. Can you try asking a more specific physics-related question?"

    # Add context to chat history
    chatHistory.append(HumanMessage(content=context))

    # Create prompt using chat history
    prompt = ChatPromptTemplate.from_messages(chatHistory)
    
    # Create output parser
    parser = StrOutputParser()

    # Chain prompt, model, and parser
    try:
        chain = prompt | ollama_model | parser
        response = chain.invoke({})  # Assuming invoke() works like this with the model
    except Exception as e:
        return f"Error generating response: {e}"

    # Add AI response to chat history
    chatHistory.append(AIMessage(content=response))

    return response

# To clear chat history for a new session
def clear_chat_history():
    chatHistory.clear()
    chatHistory.append(SystemMessage(content=systemMessage))
