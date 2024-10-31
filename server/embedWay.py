import json
import os
from scipy.spatial.distance import cosine
from chromadb import chromadb
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Initialize the embedding model
embedding = OllamaEmbeddings(model="nomic-embed-text:latest")

# Directory and paths
output_dir = r"D:\SUMMER24\CSE299[NBM]\project"
similarity_output_path = os.path.join(output_dir, "cosine_similarity_scores.json")

# Helper function to calculate cosine similarity
def cosine_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)

# Load chatbot and expected answer JSON files and generate embeddings
similarity_scores = []

for i in range(1, 17):
    # Load the chatbot and expected output files
    llm_file_path = f"llm_output{i}.json"
    expected_file_path = f"output{i}.json"
    
    with open(llm_file_path, encoding="utf-8") as llm_file, open(expected_file_path, encoding="utf-8") as expected_file:
        llm_output = json.load(llm_file)
        expected_output = json.load(expected_file)

    # Iterate through each answer and compute cosine similarity
    for chapter, expected_chapter in zip(llm_output, expected_output):
        for topic, expected_topic in zip(chapter["topics"], expected_chapter["topics"]):
            for typ, expected_typ in zip(topic["types"], expected_topic["types"]):
                for question_data, expected_question_data in zip(typ["questions"], expected_typ["questions"]):
                    # Get main question text and generate embeddings
                    llm_main_text = question_data["main_question"]["a"]
                    expected_main_text = expected_question_data["main_question"]["a"]
                    llm_main_embedding = embedding.embed_query(llm_main_text)
                    expected_main_embedding = embedding.embed_query(expected_main_text)
                    
                    # Calculate and store cosine similarity for main question
                    main_similarity = cosine_similarity(llm_main_embedding, expected_main_embedding)
                    similarity_entry = {
                        "file": f"llm_output{i}.json",
                        "question": question_data["main_question"]["q"],
                        "similarity_score": main_similarity,
                    }

                    # Calculate and store cosine similarity for follow-up questions if present
                    follow_up_similarities = []
                    for follow_up, expected_follow_up in zip(
                        question_data.get("follow_up_questions", []), 
                        expected_question_data.get("follow_up_questions", [])
                    ):
                        follow_up_text = follow_up["a"]
                        expected_follow_up_text = expected_follow_up["a"]
                        follow_up_embedding = embedding.embed_query(follow_up_text)
                        expected_follow_up_embedding = embedding.embed_query(expected_follow_up_text)

                        follow_up_similarity = cosine_similarity(follow_up_embedding, expected_follow_up_embedding)
                        follow_up_similarities.append({
                            "question": follow_up["q"],
                            "similarity_score": follow_up_similarity,
                        })
                    
                    similarity_entry["follow_up_similarities"] = follow_up_similarities
                    similarity_scores.append(similarity_entry)

# Save results to a JSON file
with open(similarity_output_path, "w", encoding="utf-8") as file:
    json.dump(similarity_scores, file, indent=4, ensure_ascii=False)

print(f"Similarity scores have been saved to {similarity_output_path}")
