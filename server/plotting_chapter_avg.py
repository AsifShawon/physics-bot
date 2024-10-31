import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import seaborn as sns
import os
import re

# Directory containing JSON files and the output directory for the plot
output_dir = r"D:\SUMMER24\CSE299[NBM]\project"
output_path = os.path.join(output_dir, "average_chapter_plot.png")

# Initialize data structure to store cumulative scores by chapter
cumulative_scores_by_chapter = defaultdict(list)

# Loop through files 1 to 14 and accumulate scores
for i in range(1, 15):
    file_path = f"test_output{i}.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Accumulate scores by chapter and topic
    for chapter in data:
        chapter_name = chapter["chapter"]
        
        # Extract only the chapter number (e.g., "13" from "13 - MODERN PHYSICS AND ELECTRONICS")
        print(chapter_name)
        chapter_number = re.match(r'(\d+)', chapter_name).group(1)

        chapter_scores = []

        for topic in chapter["topics"]:
            # Extract all scores for main questions and follow-ups
            for typ in topic["types"]:
                for question in typ["questions"]:
                    # Main question score
                    main_score = question["main_question"]["score"]
                    chapter_scores.append(main_score)

                    # Follow-up questions scores
                    for follow_up in question["follow_up_questions"]:
                        follow_up_score = follow_up["score"]
                        chapter_scores.append(follow_up_score)

        # Add the average score for this chapter in the current file to the cumulative list
        if chapter_scores:
            chapter_avg = np.mean(chapter_scores)
            cumulative_scores_by_chapter[chapter_number].append(chapter_avg)

# Prepare data for plotting
chapters = sorted(cumulative_scores_by_chapter.keys(), key=int)  # Sort numerically
chapter_averages = [np.mean(cumulative_scores_by_chapter[chapter]) for chapter in chapters]

# Generate a color palette for the chapters
colors = sns.color_palette("husl", len(chapters))

# Create the plot
plt.figure(figsize=(12, 6))

# Plot average scores for each chapter
bars = plt.bar(chapters, chapter_averages, color=colors, alpha=0.7)

# Customize the plot
plt.xlabel('Chapter Number', fontsize=12)
plt.ylabel('Average Score', fontsize=12)
plt.title('Average Scores by Chapter', fontsize=14, pad=20)

# Add grid for better readability
plt.grid(True, axis='y', linestyle='--', alpha=0.3)

# Add numerical labels on top of each bar
for bar, avg_score in zip(bars, chapter_averages):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, round(avg_score, 2), ha='center', va='bottom')

# Save the plot
plt.tight_layout()
plt.savefig(output_path)
plt.close()

print(f"Saved average chapter plot to {output_path}")
