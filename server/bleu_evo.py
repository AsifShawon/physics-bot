import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk

# Load NLTK resources
nltk.download('punkt')

# BLEU score function with smoothing
def calculate_bleu_score(reference: str, candidate: str) -> float:
    reference_tokens = [nltk.word_tokenize(reference)]
    candidate_tokens = nltk.word_tokenize(candidate)
    
    # Use smoothing function to handle cases with low or zero higher-order n-grams
    smoothing_fn = SmoothingFunction().method1
    bleu_score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothing_fn)
    
    return bleu_score * 100  # Scale to 0-100 range


# Helper function to get answers from both LLM and expected data
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

                    for expected_chapter in expected_data:
                        for expected_topic in expected_chapter.get("topics", []):
                            if topic["topic"] == expected_topic["topic"]:
                                for expected_type in expected_topic.get("types", []):
                                    if typ["type"] == expected_type["type"]:
                                        for expected_question in expected_type.get("questions", []):
                                            expected_main_question = expected_question["main_question"]

                                            if llm_main_question["q"].strip() == expected_main_question["q"].strip():
                                                main_question_data = {
                                                    "main_question": {
                                                        "q": llm_main_question["q"],
                                                        "llm_answer": llm_answer_main,
                                                        "expected_answer": expected_main_question["a"].strip(),
                                                        "bleu_score": calculate_bleu_score(
                                                            expected_main_question["a"].strip(), llm_answer_main
                                                        )
                                                    },
                                                    "follow_up_questions": []
                                                }

                                                # Add follow-up questions if available
                                                llm_follow_ups = question_data.get("follow_up_questions", [])
                                                expected_follow_ups = expected_question.get("follow_up_questions", [])

                                                for llm_follow_up, expected_follow_up in zip(llm_follow_ups, expected_follow_ups):
                                                    if llm_follow_up["q"].strip() == expected_follow_up["q"].strip():
                                                        follow_up_data = {
                                                            "q": llm_follow_up["q"],
                                                            "llm_answer": llm_follow_up["a"].strip(),
                                                            "expected_answer": expected_follow_up["a"].strip(),
                                                            "bleu_score": calculate_bleu_score(
                                                                expected_follow_up["a"].strip(), llm_follow_up["a"].strip()
                                                            )
                                                        }
                                                        main_question_data["follow_up_questions"].append(follow_up_data)

                                                type_data["questions"].append(main_question_data)
                topic_data["types"].append(type_data)
            chapter_data["topics"].append(topic_data)
        results.append(chapter_data)
    return results

# Load JSON data and collect answers with BLEU scores
for file_no in range(1, 17):
    llm_file_path = f"llm_output{file_no}.json"
    expected_file_path = f"output{file_no}.json"
    
    with open(llm_file_path, encoding="utf-8") as llm_file, open(expected_file_path, encoding="utf-8") as expected_file:
        llm_output = json.load(llm_file)
        expected_output = json.load(expected_file)

    evaluated_answers = get_all_answers(llm_output, expected_output)

    # Save results to JSON file
    output_file_path = f"test_bleu_output{file_no}.json"
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(evaluated_answers, output_file, indent=4, ensure_ascii=False)
    
    print(f"Processed and saved results for file {file_no} to {output_file_path}")
