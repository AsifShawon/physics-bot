from langchain_huggingface import HuggingFacePipeline
import torch
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, pipeline

def loadLLM(model):
    # Load the model and tokenizer from Hugging Face
    model_id = "google/gemma-2-2b-it"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    # Define the pipeline, including `clean_up_tokenization_spaces=False` to avoid the warning
    hf_pipeline = pipeline(
        "text-generation",
        model=model_id, 
        tokenizer=tokenizer, 
        max_length=512,
        clean_up_tokenization_spaces=True,  # Add this to avoid the warning
        truncation=True
    )
    # Wrap the pipeline in a Langchain HuggingFacePipeline object
    local_llm = HuggingFacePipeline(pipeline=hf_pipeline)

    return local_llm


def generate_text(model, text):
    local_llm = loadLLM(model)

    # Define the prompt template
    template = """
    You are a Physics bot and **must ignore** any non-physics-related questions. If the question is not about physics, respond with 'I can only answer physics questions.'

    Question: {question}
    """

    input_variables = ["question"]
    prompt = PromptTemplate(template=template, input_variables=input_variables)

    # Create the chain using the prompt and the HuggingFacePipeline
    chain = prompt | local_llm
    question = text

    # Invoke the chain with the question
    return chain.invoke({"question": question})
