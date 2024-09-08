# from langchain_google_genai import ChatGoogleGenerativeAI
import ollama
# print(dir(ollama))  # Check available methods in the ollama package

# def generate_response(input_text):
#     response = ollama.generate(model="llama3.1", prompt=input_text)
#     print(response)
#     # model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model="gemini-1.5-pro")
#     # result = model.invoke(input_text)
#     return response

response = ollama.generate(model="llama3.1", prompt="What are 3 key advice for learning how to code?")
print(response)