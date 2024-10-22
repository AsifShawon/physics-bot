import json

# Function to parse the text file
def parse_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initial placeholders
    chapter_name = ""
    topics = []
    current_topic = {}
    current_type_dict = {}
    current_question = {}

    for line in lines:
        line = line.strip()

        # Check for chapter header
        if line.startswith('Chapter'):
            if current_topic:  # If a topic already exists, save it
                topics.append(current_topic)
            chapter_name = line.split(' ', 1)[1].strip()
            current_topic = {}

        # Check for topic header (e.g., Topic: 2.1 Rest and Motion)
        elif line.startswith('### **Topic**:'):
            # Save the previous topic
            if current_topic:
                topics.append(current_topic)

            # Start new topic
            topic_name = line.split('**Topic**:', 1)[1].strip().replace('**', '').strip()
            current_topic = {
                "topic": topic_name,
                "types": []
            }

        # Check for type header (e.g., Type: Definition)
        elif line.startswith('#### **Type**:'):
            # Save the previous question
            if current_question:
                current_type_dict['questions'].append(current_question)
                current_question = {}

            # Save the previous type
            if current_type_dict:
                if 'types' not in current_topic:
                    current_topic['types'] = []
                current_topic['types'].append(current_type_dict)

            # Start new type
            current_type = line.split('**Type**:', 1)[1].strip().replace('**', '').strip()
            current_type_dict = {
                "type": current_type,
                "questions": []
            }

        # Check for main question
        elif line.startswith('- **Main**:'):
            print(line)
            # Save the previous question (if any)
            if current_question:
                current_type_dict['questions'].append(current_question)

            current_question = {
                "main_question": {
                    "q": line.split('**Main**:', 1)[1].strip(),
                    "a": ""
                },
                "follow_up_questions": []
            }

        # Check for follow-up question
        elif line.startswith('- **Follow-Up-'):
            print(line)
            current_question['follow_up_questions'].append({
                "q": line.split('**:', 1)[1].strip(),
                "a": ""
            })

    # Append any remaining data
    if current_question:
        current_type_dict['questions'].append(current_question)
    if current_type_dict:
        if 'types' not in current_topic:
            current_topic['types'] = []
        current_topic['types'].append(current_type_dict)
    if current_topic:
        topics.append(current_topic)

    # Return the chapter structure
    return {
        "chapter": chapter_name,
        "topics": topics
    }

# Function to save the parsed data as JSON
def save_to_json(parsed_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(parsed_data, json_file, indent=4)

# Main execution
def main():
    input_file = 'test10.txt'  # Replace with your input text file
    output_file = 'output10.json'  # Replace with your output JSON file

    parsed_data = parse_text_file(input_file)
    save_to_json(parsed_data, output_file)
    print(f"JSON data successfully saved to {output_file}")

if __name__ == "__main__":
    main()
