from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = "AIzaSyAfBDLnOerYntiLjmwA0PmJ-yZmN5LvCJ0"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)
response = llm.invoke("What is the speed of light?")

print(response.content)