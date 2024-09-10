from langchain_huggingface import HuggingFacePipeline
import torch
from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Load the model and tokenizer from Hugging Face
model_id = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, device_map='auto')

# Define the pipeline, including `clean_up_tokenization_spaces=False` to avoid the warning
hf_pipeline = pipeline(
    "text2text-generation",
    model=model, 
    tokenizer=tokenizer, 
    max_length=128,
    clean_up_tokenization_spaces=True  # Add this to avoid the warning
)

# Wrap the pipeline in a Langchain HuggingFacePipeline object
local_llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Define the prompt template
template = """You are a Physics bot and answer only physics questions and in English.
Question: {question}
"""
input_variables = ["question"]
prompt = PromptTemplate(template=template, input_variables=input_variables)

# Create the chain using the prompt and the HuggingFacePipeline
chain = prompt | local_llm
question = "What is the formula for the force of gravity?"

# Invoke the chain with the question
print("Ans: ", local_llm.invoke(question))
