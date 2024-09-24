from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search

chatHistory = []
systemMessage = "You are a helpful physics assistant. You are given documents from a physics book to help answer the questions. If the answer is not in the documents, respond with 'I'm not sure'. Do not respond to questions unrelated to physics."

chatHistory.append(SystemMessage(content=systemMessage))

def generate_text(model, query):
    # Retrieve context from physics documents
    retrieved_text = search(query)

    if retrieved_text:
        context = (f"Here are some documents that might help answer the question: \n{retrieved_text}\n"
                   f"Answer the question: {query} based on these documents. If the answer is not found in the documents, respond with 'I'm not sure'.")
    else:
        context = f"The question is: {query}. "

    # Add to chat history and generate response
    chatHistory.append(HumanMessage(content=context))
    model = Ollama(model=model)
    prompt = ChatPromptTemplate.from_messages(chatHistory)
    parser = StrOutputParser()

    # Chain the prompt, model, and parser
    chain = prompt | model | parser
    response = chain.invoke({})

    # Add the response to chat history
    chatHistory.append(AIMessage(content=response))

    return response

# To clear chat history for a new session
def clear_chat_history():
    chatHistory.clear()
    chatHistory.append(SystemMessage(content=systemMessage))
