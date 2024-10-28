import json
import time
from OllamaLLM import generate_text, clear_chat_history  # Assuming this function retrieves the answers

# Load JSON data from file
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Save JSON data to file
def save_json_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Main function to get answers and save them back to JSON
def get_reply_and_save(json_file):
    json_data = load_json_data(json_file)

    # Iterate through the structure of the JSON
    for chapter in json_data:
        if 'topics' in chapter:  # Check if 'topics' exists
            for topic in chapter['topics']:
                if 'types' in topic:  # Check if 'types' exists within the topic
                    for type_obj in topic['types']:
                        if 'questions' in type_obj:  # Check if 'questions' exist
                            for question_obj in type_obj['questions']:
                                # Handle main question
                                if 'main_question' in question_obj:
                                    main_question = question_obj['main_question']['q']
                                    start_time = time.time()  # Start the timer
                                    main_answer = generate_text(main_question)  # Get the answer for the main question
                                    end_time = time.time()  # End the timer
                                    response_time = end_time - start_time  # Calculate the time taken

                                    # Save answer and response time
                                    question_obj['main_question']['a'] = main_answer
                                    question_obj['main_question']['time_taken'] = response_time

                                # Handle follow-up questions
                                if 'follow_up_questions' in question_obj:
                                    for follow_up in question_obj['follow_up_questions']:
                                        follow_up_question = follow_up['q']
                                        start_time = time.time()  # Start the timer for follow-up
                                        follow_up_answer = generate_text(follow_up_question)  # Get the answer for the follow-up
                                        end_time = time.time()  # End the timer
                                        response_time = end_time - start_time  # Calculate the time taken

                                        # Save follow-up answer and response time
                                        follow_up['a'] = follow_up_answer
                                        follow_up['time_taken'] = response_time
                                    save_json_data("llm_replied.json", json_data)
                                    return

                                
                else:
                    print(f"Warning: 'types' key not found in topic: {topic}")
                
        else:
            print(f"Warning: 'topics' key not found in chapter: {chapter}")
        
        clear_chat_history()  # Clear chat history for the next question

    # Save the updated JSON data back to the file
    save_json_data("llm_output1.json", json_data)

# Call the function
get_reply_and_save('output1.json')
