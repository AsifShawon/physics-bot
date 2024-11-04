import json
import os
import re

# Helper function to extract topic number
def extract_topic_number(topic_name):
    match = re.match(r"(\d+\.\d+)", topic_name)
    return match.group(1) if match else None

# Load data from output16.json
with open("llm_output16.json", "r", encoding="utf-8") as f:
    output16_data = json.load(f)

# Create a dictionary for easy access to calculation data by chapter and topic number
calculation_data_by_chapter_topic = {}
for chapter_data in output16_data:
    chapter_name = chapter_data["chapter"].lower()
    print(f"Processing chapter: {chapter_name}")
    topics_data = {}
    for topic in chapter_data["topics"]:
        topic_number = extract_topic_number(topic["topic"])  # Extract topic number
        if topic_number:
            for type_data in topic["types"]:
                if type_data["type"] == "Calculation":
                    topics_data[topic_number] = type_data["questions"]
                    print(f"Found Calculation questions for topic number: {topic_number}")
    calculation_data_by_chapter_topic[chapter_name] = topics_data

# Process each output[1-13].json file
for file_no in range(1, 14):
    file_path = f"llm_output{file_no}.json"
    
    # Load data from the current output file
    with open(file_path, "r", encoding="utf-8") as f:
        chapter_data = json.load(f)
    
    # Get the current chapter name to match with output16.json
    chapter_name = chapter_data[0]["chapter"].lower()
    
    # Check if calculation data exists for this chapter in output16.json
    if chapter_name in calculation_data_by_chapter_topic:
        # Get the Calculation questions by topic number for this chapter
        calculation_topics_data = calculation_data_by_chapter_topic[chapter_name]
        
        # For each topic in the chapter, add the Calculation type if it exists in output16.json
        for topic in chapter_data[0]["topics"]:
            topic_number = extract_topic_number(topic["topic"])  # Extract topic number
            if topic_number and topic_number in calculation_topics_data:
                # Add the Calculation type only if it doesn't already exist in this topic
                if not any(t["type"] == "Calculation" for t in topic["types"]):
                    print(f"Adding Calculation questions for topic number: {topic_number}")
                    calculation_type_data = {
                        "type": "Calculation",
                        "questions": calculation_topics_data[topic_number]
                    }
                    topic["types"].append(calculation_type_data)
    
    # Save the modified data back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chapter_data, f, indent=4, ensure_ascii=False)

    print(f"Processed and updated {file_path}")
