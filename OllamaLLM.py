from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OllamaEmbeddings


def generate_text(model,text):
    model  = Ollama(model = model)
    parser = StrOutputParser()
    chain = model | parser
    response = chain.invoke(text)

    return response