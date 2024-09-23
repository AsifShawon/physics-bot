from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate 
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search


chatHistory = []
systemMessage = "You are a helpful physics assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. You only answer physics-related questions and ignore any non-physics-related questions. If the question is not about physics, respond with 'I can only answer physics questions.'"
chatHistory.append(SystemMessage(content=systemMessage))

def generate_text(model, query):

    # context from physics documents
    retrieved_text = search(query)
    context = ("Here are some documents that might help you answer better: \n"
               + query + "\n"
               + retrieved_text)
    
    chatHistory.append(HumanMessage(content=context))
    model = Ollama(model=model)
    prompt = ChatPromptTemplate.from_messages(chatHistory)
    parser = StrOutputParser()
    
    chain = prompt | model | parser
    
    response = chain.invoke({})
    chatHistory.append(AIMessage(content=response))
    
    # for msg in chatHistory:
    #     print(f"{msg.type}: {msg.content}")
    
    return response

# Test with your model and input
# response = generate_text("gemma2:2b", "What is the speed of light?")
# print(response)
def clear_chat_history():
    chatHistory.clear()
    systemMessage = "You are a helpful physics assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. You only answer physics-related questions and ignore any non-physics-related questions. If the question is not about physics, respond with 'I can only answer physics questions.'"
    chatHistory.append(SystemMessage(content=systemMessage))
