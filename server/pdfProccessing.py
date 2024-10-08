import fitz  # PyMuPDF
import re
import json
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_extracted_text(text: str) -> str:
    """
    Cleans up the extracted text by fixing special character encodings, 
    formatting numbers, and removing unnecessary line breaks.
    """
    # Replace the multiplication sign encoded as \u00d7 with the actual symbol
    text = text.replace('\u00d7', '×')
    
    # Fix numbers like "3 10" into "3 × 10^" (scientific notation fix)
    text = re.sub(r"(\d+)\s+(\d+)\s+10", r"\1 × 10^\2", text)

    # Fix broken lines by merging lines that end abruptly
    text = re.sub(r"([a-z0-9])-?\n([a-zA-Z0-9])", r"\1\2", text)

    # Remove unnecessary line breaks and extra spaces
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # Fix spacing around mathematical operators
    text = re.sub(r'(\d+)\s*([+\-×÷=])\s*(\d+)', r'\1 \2 \3', text)

    return text

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts the full text from the PDF and cleans it up."""
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join(clean_extracted_text(page.get_text("text")) for page in doc)
        logging.debug(f"Extracted and cleaned text (first 500 chars): {text[:500]}")
        # save text with utf-8 encoding
        with open("Physics.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def split_into_chapters(text: str) -> List[Dict[str, str]]:
    """Splits text into chapters based on chapter number and title."""
    chapter_pattern = r"(Chapter \w+)\s*\n([A-Z][A-Z\s]+)"
    logging.debug(f"Searching for chapter pattern: {chapter_pattern}")
    matches = list(re.finditer(chapter_pattern, text, re.MULTILINE))
    logging.debug(f"Number of chapter matches found: {len(matches)}")
    
    if not matches:
        logging.warning("No chapters found in the text.")
        logging.debug(f"Text snippet (first 1000 chars):\n{text[:1000]}")
        return []

    chapters = []
    for i, match in enumerate(matches):
        chapter_no, chapter_title = match.groups()
        start_pos = match.start()
        end_pos = matches[i+1].start() if i < len(matches) - 1 else len(text)
        
        chapter_data = {
            'chapter': chapter_no.capitalize(),
            'title': chapter_title.strip(),
            'data': text[start_pos:end_pos].strip()
        }
        chapters.append(chapter_data)
        logging.debug(f"Found chapter: {chapter_data['chapter']} - {chapter_data['title']}")
    
    return chapters

import re

def chunk_chapter_by_topics(chapter_data: str, chapter_number: int) -> List[Dict[str, str]]:
    """Further splits a chapter into smaller chunks based on topic headings and formats math expressions in Markdown."""
    topic_pattern = rf"{chapter_number}\.(\d+)(?:\s*[:.]?)\s+([A-Z][A-Za-z\s]+)"
    logging.debug(f"Searching for topic pattern: {topic_pattern}")
    matches = list(re.finditer(topic_pattern, chapter_data, re.MULTILINE))
    logging.debug(f"Number of potential topic matches found: {len(matches)}")
    
    if not matches:
        logging.warning(f"No topics found in Chapter {chapter_number}.")
        return [{'topic': 'Untitled', 'data': chapter_data.strip()}]

    chunks = []
    last_topic_number = 0

    ignore_patterns = [
        rf"Figure:\s*{chapter_number}\.\d+",
        rf"Fig:\s*{chapter_number}\.\d+",
        rf"\({chapter_number}\.\d+\)",
        rf"^{chapter_number}\.\d+$"  # Matches standalone numbers like "8.1"
    ]
    ignore_regex = re.compile('|'.join(ignore_patterns), re.IGNORECASE)

    for match in matches:
        topic_number = int(match.group(1))
        topic_title = match.group(2).strip()

        # Skip ignored topics
        if ignore_regex.search(topic_title):
            continue

        # Sequential check
        if topic_number != last_topic_number + 1:
            logging.warning(f"Non-sequential topic number found: {chapter_number}.{topic_number}")
            continue

        start_pos = match.start()
        next_topic_pattern = rf"{chapter_number}\.{topic_number + 1}(?:\s*[:.])"
        end_pos = re.search(next_topic_pattern, chapter_data[start_pos:])
        if end_pos:
            end_pos = start_pos + end_pos.start()
        else:
            end_pos = len(chapter_data)

        topic_content = chapter_data[start_pos:end_pos].strip()

        # Process Math Expressions for Markdown:
        topic_content = convert_math_to_markdown(topic_content)

        chunk_data = {
            'topic': f"{chapter_number}.{topic_number} {topic_title}",
            'data': topic_content
        }
        chunks.append(chunk_data)
        last_topic_number = topic_number

    return chunks

def convert_math_to_markdown(text: str) -> str:
    """Converts math expressions in text to LaTeX-style Markdown."""
    # Convert inline math expressions (e.g., E = mc^2)
    # You can adjust this based on your specific math content pattern
    inline_math_pattern = r"\[(.*?)\]"  # Assuming math is within brackets [E = mc^2]
    text = re.sub(inline_math_pattern, r'$\1$', text)

    # Convert block math expressions (for larger expressions)
    block_math_pattern = r"\$\$(.*?)\$\$"  # Assuming block math is between $$
    text = re.sub(block_math_pattern, r'$$\1$$', text)

    return text


def process_and_chunk_pdf(pdf_path: str, output_file: str) -> None:
    """Process the PDF, split it into chapters, then chunk each chapter by topics."""
    try:
        pdf_text = extract_text_from_pdf(pdf_path)
        chapters = split_into_chapters(pdf_text)
        
        if not chapters:
            logging.error("No chapters found. Cannot proceed with processing.")
            return

        for i, chapter in enumerate(chapters, 1):
            chapter['chunks'] = chunk_chapter_by_topics(chapter['data'], i)
            del chapter['data']
        
        save_to_json(chapters, output_file)
        logging.info(f"Successfully processed PDF and saved results to {output_file}")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        raise

def save_to_json(data: List[Dict], output_file: str) -> None:
    """Save the data to a JSON file."""
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving to JSON: {e}")
        raise

if __name__ == "__main__":
    pdf_path = "Physics.pdf"
    output_file = "chunked_physics_data.json"

    process_and_chunk_pdf(pdf_path, output_file)

    # Optional: Print a sample chunk
    try:
        with open(output_file, 'r') as f:
            chunked_data = json.load(f)
        if chunked_data and chunked_data[0].get('chunks'):
            print(json.dumps(chunked_data[0]['chunks'][0], indent=4))
        else:
            print("No chunks found in the first chapter.")
    except Exception as e:
        logging.error(f"Error reading or displaying sample chunk: {e}")