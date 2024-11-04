import json
import os

# Define keywords for each category
conceptual_keywords = ["Definition", "Conceptual", "Explanation", "Examples", "Understanding"]
mathematical_keywords = ["Calculation", "Numerical", "Problem-solving", "Equation", "Formula", "Analytical", "Graphical"]

# Initialize containers for each category
conceptual_data = []
mathematical_data = []
general_data = []

# Function to categorize questions and organize them by chapter and topic
def categorize_questions(chapter_data, conceptual_data, mathematical_data, general_data):
    chapter_name = chapter_data['chapter']
    
    # Create entries for each category for the current chapter
    conceptual_entry = {"chapter": chapter_name, "topics": []}
    mathematical_entry = {"chapter": chapter_name, "topics": []}
    general_entry = {"chapter": chapter_name, "topics": []}

    for topic in chapter_data['topics']:
        topic_name = topic['topic']
        
        # Initialize lists for questions of each category under the current topic
        conceptual_questions = []
        mathematical_questions = []
        general_questions = []
        
        for typ in topic['types']:
            question_type = typ['type']
            questions = typ["questions"]
            
            # Categorize based on type keywords
            if any(keyword in question_type for keyword in conceptual_keywords):
                conceptual_questions.extend(questions)
            elif any(keyword in question_type for keyword in mathematical_keywords):
                mathematical_questions.extend(questions)
            else:
                general_questions.extend(questions)
        
        # Add topic to each category entry only if it has questions in that category
        if conceptual_questions:
            conceptual_entry["topics"].append({
                "topic": topic_name,
                "questions": conceptual_questions
            })
        if mathematical_questions:
            mathematical_entry["topics"].append({
                "topic": topic_name,
                "questions": mathematical_questions
            })
        if general_questions:
            general_entry["topics"].append({
                "topic": topic_name,
                "questions": general_questions
            })
    
    # Append chapter entries to respective lists if they contain topics
    if conceptual_entry["topics"]:
        conceptual_data.append(conceptual_entry)
    if mathematical_entry["topics"]:
        mathematical_data.append(mathematical_entry)
    if general_entry["topics"]:
        general_data.append(general_entry)

# Process each chapter file and categorize questions
for file_no in range(1, 15):  # Files output1.json to output14.json
    file_path = f"test_output{file_no}.json"
    
    # Load each chapter data
    with open(file_path, "r", encoding="utf-8") as f:
        chapter_data = json.load(f)
    
    # Categorize each question by type for the chapter
    for chapter in chapter_data:
        categorize_questions(chapter, conceptual_data, mathematical_data, general_data)

# Save categorized data to JSON files with specified format
with open('category_conceptual_output.json', 'w', encoding='utf-8') as file:
    json.dump(conceptual_data, file, indent=4, ensure_ascii=False)

with open('category_mathematical_output.json', 'w', encoding='utf-8') as file:
    json.dump(mathematical_data, file, indent=4, ensure_ascii=False)

with open('category_general_output.json', 'w', encoding='utf-8') as file:
    json.dump(general_data, file, indent=4, ensure_ascii=False)

print("Categorized data saved into category_conceptual_output.json, category_mathematical_output.json, and category_general_output.json.")
