import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import seaborn as sns
import os
import re

# Directory containing JSON files and the output directory for the plots
output_dir = r"D:\SUMMER24\CSE299[NBM]\project"

# Loop through files 1 to 14 to generate a plot for each chapter
for i in range(1, 16):
    file_path = f"test_output{i}.json"
    output_path = os.path.join(output_dir, f"chapter_{i}_plot.png")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract scores by topic for each chapter
    for chapter in data:
        chapter_name = chapter["chapter"]
        
        # Extract chapter number (e.g., "13" from "13 - MODERN PHYSICS AND ELECTRONICS")
        chapter_number = re.match(r'(\d+)', chapter_name).group(1)

        question_scores = []
        topic_colors = {}
        topic_averages = {}
        x_positions = []
        x_ticks = []
        
        # Assign a unique color for each topic and gather scores
        topics = {topic["topic"]: [] for topic in chapter["topics"]}
        colors_palette = sns.color_palette("husl", len(topics))  # Use a distinct variable for color palette
        
        # Map topics to colors and compute scores for each question
        topic_num = 1
        pos = 0  # x-position for bars
        for (topic_name, color), topic_data in zip(topics.items(), chapter["topics"]):
            # Convert color to RGBA explicitly
            color = tuple(sns.color_palette("husl", len(topics))[topic_num - 1])
            topic_colors[topic_name] = color

            # Collect scores for each question in this topic
            topic_scores = []
            for typ in topic_data["types"]:
                for question in typ["questions"]:
                    # Main question score
                    main_score = question["main_question"]["score"]
                    question_scores.append((pos, main_score, color, topic_num))
                    topic_scores.append(main_score)
                    x_positions.append(pos)
                    pos += 1

                    # Follow-up question scores
                    for follow_up in question["follow_up_questions"]:
                        follow_up_score = follow_up["score"]
                        question_scores.append((pos, follow_up_score, color, topic_num))
                        topic_scores.append(follow_up_score)
                        x_positions.append(pos)
                        pos += 1

            # Store average for topic and set x-tick label in the middle of the topic group
            topic_avg = np.mean(topic_scores)
            topic_averages[topic_num] = topic_avg
            x_ticks.append((x_positions[-1] + x_positions[-len(topic_scores)]) // 2)
            
            topic_num += 1

        # Separate data for plotting
        x_labels = [str(i + 1) for i in range(len(x_positions))]  # Just numbering questions
        scores = [q[1] for q in question_scores]
        bar_colors = [q[2] for q in question_scores]  # Explicitly use 'bar_colors' with RGBA colors
        topic_nums = [q[3] for q in question_scores]  # Just topic numbers on x-axis

        # Create the plot for the chapter
        plt.figure(figsize=(14, 7))

        # Plot each question score, color-coded by topic
        bars = plt.bar(x_positions, scores, color=bar_colors, alpha=0.7)

        # Plot average line for each topic
        for topic_num, avg in topic_averages.items():
            topic_positions = [pos for pos, _, _, t_num in question_scores if t_num == topic_num]
            plt.plot(topic_positions, [avg] * len(topic_positions), color='blue', linewidth=2, label='Topic Average' if topic_num == 1 else "")

        # Customize the plot
        plt.xlabel('Topic Number', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.title(f'Chapter {chapter_number} - {chapter_name}', fontsize=14, pad=20)

        # Set x-ticks at the center of each topic group
        plt.xticks(x_ticks, [f"Topic {num}" for num in range(1, len(topic_averages) + 1)], rotation=45, ha='right')

        # Add grid for better readability
        plt.grid(True, axis='y', linestyle='--', alpha=0.3)

        # Add a legend with topic colors at the bottom
        legend_elements = [plt.Line2D([0], [0], color='blue', marker='o', label='Topic Average', linewidth=2)] + \
                          [plt.Rectangle((0, 0), 1, 1, facecolor=topic_colors[name], label=f"Topic {num}") for num, name in enumerate(topic_colors, 1)]
        plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, title="Legend")

        # Save the plot for this chapter
        plt.tight_layout(rect=[0, 0.1, 1, 1])  # Add space at bottom for legend
        plt.savefig(output_path)
        plt.close()

        print(f"Saved plot for Chapter {chapter_number} to {output_path}")
