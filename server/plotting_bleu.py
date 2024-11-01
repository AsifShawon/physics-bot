import json
import matplotlib.pyplot as plt
import numpy as np

# Initialize lists to store average BLEU scores per file
file_scores = []
file_names = []

# Loop through each output file to load BLEU scores
for file_no in range(1, 17):
    file_path = f"test_bleu_output{file_no}.json"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Collect BLEU scores for each question in the file
    bleu_scores = []
    for chapter in data:
        for topic in chapter["topics"]:
            for typ in topic["types"]:
                for question_data in typ["questions"]:
                    # Add main question BLEU score
                    main_bleu_score = question_data["main_question"]["bleu_score"]
                    bleu_scores.append(main_bleu_score)
                    
                    # Add follow-up question BLEU scores
                    for follow_up in question_data["follow_up_questions"]:
                        follow_up_bleu_score = follow_up["bleu_score"]
                        bleu_scores.append(follow_up_bleu_score)
    
    # Calculate the average BLEU score for this file
    avg_bleu_score = np.mean(bleu_scores) if bleu_scores else 0
    file_scores.append(avg_bleu_score)
    file_names.append(f"File {file_no}")

# Plot the BLEU scores
plt.figure(figsize=(12, 6))
plt.plot(file_names, file_scores, marker='o', color='b', linestyle='-', linewidth=2)
plt.xlabel('Files')
plt.ylabel('Average BLEU Score')
plt.title('Average BLEU Scores per File')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
