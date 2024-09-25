from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search

# Initialize chat history and system message
chatHistory = []
systemMessage = "You are a helpful physics assistant. You are given documents from a physics book to help answer the questions. If the answer is not in the documents, respond with 'I'm not sure'. Do not respond to questions unrelated to physics."
chatHistory.append(SystemMessage(content=systemMessage))

# Initialize model once
ollama_model = Ollama(model="llama3.2:3b")

def generate_text(query):
    # Retrieve context from physics documents
    retrieved_text = search(query)

    if retrieved_text:
        context = (f"Here are some documents that might help answer the question: \n{retrieved_text}\n"
                   f"Answer the question: {query} based on these documents. Do the maths properly. If the answer is not found in the documents, respond with 'Ask me physics related question'.")
    else:
        context = f"The question is: {query}. "

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
