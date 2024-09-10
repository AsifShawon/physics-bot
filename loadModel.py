from langchain_huggingface.llms import HuggingFacePipeline

hf = HuggingFacePipeline.from_model_id(
    # model_id="gpt2",
    model_id="google/gemma-2-2b-it",
    task="text-generation",
    pipeline_kwargs={"max_new_tokens": 10},
)