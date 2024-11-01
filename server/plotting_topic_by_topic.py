import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load JSON data
with open("test_output16.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare data for plotting
chapter_labels = []
chapter_averages = []
topic_colors = {}
all_topic_scores = []

# Unique color for each topic across chapters
topic_names = {topic["topic"] for chapter in data for topic in chapter["topics"]}
colors_palette = sns.color_palette("husl", len(topic_names))
topic_color_map = {name: colors_palette[i] for i, name in enumerate(topic_names)}

# Extract average score per chapter and per topic
for chapter in data:
    chapter_name = chapter["chapter"]
    chapter_labels.append(chapter_name)
    topic_scores = []

    for topic in chapter["topics"]:
        topic_name = topic["topic"]
        topic_color = topic_color_map[topic_name]
        
        # Collect scores for each question within a topic
        scores = []
        for typ in topic["types"]:
            for question in typ["questions"]:
                scores.append(question["main_question"]["score"])
                scores.extend(follow_up["score"] for follow_up in question.get("follow_up_questions", []))
        
        # Calculate topic average and store with color
        if scores:
            avg_score = np.mean(scores)
            topic_scores.append(avg_score)
            all_topic_scores.append((chapter_name, topic_name, avg_score, topic_color))
    
    # Calculate overall chapter average for plotting
    chapter_avg_score = np.mean(topic_scores) if topic_scores else 0
    chapter_averages.append(chapter_avg_score)

# Plot setup
plt.figure(figsize=(18, 10))  # Increase figure size for clarity

# Plot each topic’s average score for each chapter in distinct colors
for chapter_name, topic_name, avg_score, color in all_topic_scores:
    chapter_idx = chapter_labels.index(chapter_name)
    plt.bar(chapter_idx, avg_score, color=color, label=topic_name, alpha=0.7)

# Plot overall chapter averages as blue line across chapters
plt.plot(range(len(chapter_labels)), chapter_averages, color='blue', marker='o', linewidth=2, label='Chapter Average')

# Customize the plot
plt.xlabel('Chapters', fontsize=14)
plt.ylabel('Score', fontsize=14)
plt.title('Scores by Chapter and Topic', fontsize=16, pad=20)
plt.xticks(range(len(chapter_labels)), chapter_labels, rotation=60, ha='right', fontsize=10)  # Rotate x-labels more and adjust font size
plt.grid(True, axis='y', linestyle='--', alpha=0.3)

# Add legend with unique topic colors and place it outside the plot
handles = [plt.Line2D([0], [0], color='blue', marker='o', label='Chapter Average')] + \
          [plt.Rectangle((0, 0), 1, 1, facecolor=color, label=topic) for topic, color in topic_color_map.items()]
plt.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5), title="Topics", fontsize=10)

# Save and show the plot
plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to make space for the legend on the right
plt.savefig("D:\SUMMER24\CSE299[NBM]\project\combined_chapter_plot_improved.png")
plt.show()
