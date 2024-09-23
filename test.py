from langchain_community.llms import Ollama

llm = Ollama(model="gemma2:2b")

prompt = "What is the speed of light?"
response = llm.invoke(prompt)
print(response)