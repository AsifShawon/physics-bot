import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# File paths for each category
file_paths = {
    "Conceptual": "category_conceptual_output.json",
    "General": "category_general_output.json",
    "Mathematical": "category_mathematical_output.json"
}

# Output directory for saving the plots
output_dir = "D:\\SUMMER24\\CSE299[NBM]\\project\\automated"

# Function to plot all question scores for each category file as a continuous bar plot
def plot_category_scores_as_histogram(category_name, file_path):
    # Load JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Prepare data for plotting
    question_scores = []
    chapter_start_positions = []
    chapter_numbers = []

    # Unique color for each chapter
    chapter_names = [chapter["chapter"] for chapter in data]
    colors_palette = sns.color_palette("husl", len(chapter_names))
    chapter_color_map = {name: colors_palette[i] for i, name in enumerate(chapter_names)}

    # Extract scores for each question within each chapter
    pos = 0
    for chapter in data:
        chapter_name = chapter["chapter"]
        chapter_number = chapter_name.split()[0]  # Extract chapter number
        chapter_color = chapter_color_map[chapter_name]

        # Mark the start position of the chapter for x-ticks
        chapter_start_positions.append(pos)
        chapter_numbers.append(chapter_number)

        # Collect scores for each question in the chapter
        for topic in chapter["topics"]:
            for question in topic["questions"]:
                # Main question score
                question_scores.append((pos, question["main_question"]["score"], chapter_color))
                pos += 1
                # Follow-up question scores
                for follow_up in question.get("follow_up_questions", []):
                    question_scores.append((pos, follow_up["score"], chapter_color))
                    pos += 1

    # Separate data for plotting
    x_positions = [pos for pos, _, _ in question_scores]
    scores = [score for _, score, _ in question_scores]
    colors = [color for _, _, color in question_scores]
    overall_avg_score = np.mean(scores)

    # Plot setup
    plt.figure(figsize=(18, 8))

    # Plot each question's score in a narrow bar to simulate a histogram
    plt.bar(x_positions, scores, color=colors, width=1.0)

    # Add an overall average line across all questions in the category
    plt.axhline(overall_avg_score, color='red', linestyle=':', linewidth=2, label=f'Overall Avg: {overall_avg_score:.2f}')

    # Customize the plot
    plt.xlabel('Chapters', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title(f'{category_name} Questions Scores by Chapter and Topic', fontsize=14, pad=20)

    # Set x-ticks only at the start of each chapter with chapter numbers as labels
    plt.xticks(chapter_start_positions, chapter_numbers, rotation=45, ha='right', fontsize=10)

    # Add grid for readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.3)

    # Legend with chapter colors and overall average
    legend_elements = [
        plt.Line2D([0], [0], color='red', linestyle=':', label=f'Overall Avg: {overall_avg_score:.2f}')
    ] + [
        plt.Rectangle((0, 0), 1, 1, facecolor=chapter_color_map[chapter], label=chapter)
        for chapter in chapter_names
    ]
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, title="Chapters")

    # Save the plot for this category
    output_path = f"{output_dir}/{category_name.lower()}_questions_histogram_all.png"
    plt.tight_layout(rect=[0, 0.1, 1, 1])  # Add space at bottom for legend
    plt.savefig(output_path)
    plt.close()

    print(f"Saved plot for {category_name} questions to {output_path}")

# Generate plots for each category
for category_name, file_path in file_paths.items():
    plot_category_scores_as_histogram(category_name, file_path)
