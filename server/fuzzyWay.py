import json
from fuzzywuzzy import fuzz
import spacy
import os

# Load Spacy English model
nlp = spacy.load("en_core_web_md")

# Helper function for combined similarity score
def calculate_combined_similarity(answer1: str, answer2: str) -> float:
    # Token similarity using fuzzy matching
    token_similarity = fuzz.token_set_ratio(answer1, answer2)
    
    # Semantic similarity using Spacy
    doc1 = nlp(answer1)
    doc2 = nlp(answer2)
    semantic_similarity = doc1.similarity(doc2) * 100  # Scale to 100

    # Combined score (weighted average)
    combined_score = 0.5 * token_similarity + 0.5 * semantic_similarity
    return combined_score  # Floating-point score

# Helper function to get main and follow-up answers from both LLM and expected data
def get_all_answers(llm_data, expected_data):
    results = []
    for chapter in llm_data:
        chapter_data = {"chapter": chapter["chapter"], "topics": []}
        for topic in chapter.get("topics", []):
            topic_data = {"topic": topic["topic"], "types": []}
            for typ in topic.get("types", []):
                type_data = {"type": typ["type"], "questions": []}
                for question_data in typ.get("questions", []):
                    llm_main_question = question_data["main_question"]
                    llm_answer_main = llm_main_question["a"].strip()

                    # Search for the matching expected question
                    for expected_chapter in expected_data:
                        for expected_topic in expected_chapter.get("topics", []):
                            if topic["topic"] == expected_topic["topic"]:
                                for expected_type in expected_topic.get("types", []):
                                    if typ["type"] == expected_type["type"]:
                                        for expected_question in expected_type.get("questions", []):
                                            expected_main_question = expected_question["main_question"]

                                            # Match main question and prepare results for both main and follow-up questions
                                            if llm_main_question["q"].strip() == expected_main_question["q"].strip():
                                                main_question_data = {
                                                    "main_question": {
                                                        "q": llm_main_question["q"],
                                                        "llm_answer": llm_answer_main,
                                                        "expected_answer": expected_main_question["a"].strip(),
                                                        "score": calculate_combined_similarity(llm_answer_main, expected_main_question["a"].strip())
                                                    },
                                                    "follow_up_questions": []
                                                }

                                                # Add follow-up questions if available
                                                llm_follow_ups = question_data.get("follow_up_questions", [])
                                                expected_follow_ups = expected_question.get("follow_up_questions", [])
                                                
                                                # Pair each follow-up question if question text matches
                                                for llm_follow_up, expected_follow_up in zip(llm_follow_ups, expected_follow_ups):
                                                    if llm_follow_up["q"].strip() == expected_follow_up["q"].strip():
                                                        follow_up_data = {
                                                            "q": llm_follow_up["q"],
                                                            "llm_answer": llm_follow_up["a"].strip(),
                                                            "expected_answer": expected_follow_up["a"].strip(),
                                                            "score": calculate_combined_similarity(llm_follow_up["a"].strip(), expected_follow_up["a"].strip())
                                                        }
                                                        main_question_data["follow_up_questions"].append(follow_up_data)

                                                type_data["questions"].append(main_question_data)
                topic_data["types"].append(type_data)
            chapter_data["topics"].append(topic_data)
        results.append(chapter_data)
    return results

# Loop through files 1 to 16
for file_no in range(1, 17):
    # Load JSON data from dynamically named files
    llm_file_path = f"llm_output{file_no}.json"
    expected_file_path = f"output{file_no}.json"
    
    # Check if both files exist
    if os.path.exists(llm_file_path) and os.path.exists(expected_file_path):
        with open(llm_file_path, encoding="utf-8") as llm_file, open(expected_file_path, encoding="utf-8") as expected_file:
            llm_output = json.load(llm_file)
            expected_output = json.load(expected_file)

        # Collect answers with scores
        evaluated_answers = get_all_answers(llm_output, expected_output)

        # Save results to JSON file
        output_file_path = f"test_output{file_no}.json"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(evaluated_answers, output_file, indent=4, ensure_ascii=False)
        
        print(f"Processed and saved results for file {file_no} to {output_file_path}")
    else:
        print(f"Files {llm_file_path} or {expected_file_path} not found. Skipping...")
