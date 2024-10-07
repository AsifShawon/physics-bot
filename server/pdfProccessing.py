import fitz  # PyMuPDF
import re
import json
from typing import List, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts the full text from the PDF."""
    try:
        with fitz.open(pdf_path) as doc:
            text = "\n".join(page.get_text("text") for page in doc)
        logging.debug(f"Extracted text (first 500 chars): {text[:500]}")
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
    """Further splits a chapter into smaller chunks based on topic headings."""
    # Updated pattern to match topics like "2.1 Rest and motion", "2.1: Rest and motion", or "2.1. Rest and motion"
    topic_pattern = rf"{chapter_number}\.(\d+)(?:\s*[:.]?)\s+([A-Z][A-Za-z\s]+)"
    logging.debug(f"Searching for topic pattern: {topic_pattern}")
    matches = list(re.finditer(topic_pattern, chapter_data, re.MULTILINE))
    logging.debug(f"Number of potential topic matches found: {len(matches)}")
    
    if not matches:
        logging.warning(f"No topics found in Chapter {chapter_number}.")
        return [{'topic': 'Untitled', 'data': chapter_data.strip()}]

    chunks = []
    last_topic_number = 0
    
    # Patterns to ignore
    ignore_patterns = [
        rf"Figure:\s*{chapter_number}\.\d+",
        rf"Fig:\s*{chapter_number}\.\d+",
        rf"\({chapter_number}\.\d+\)"
    ]
    ignore_regex = re.compile('|'.join(ignore_patterns), re.IGNORECASE)

    for match in matches:
        topic_number = int(match.group(1))
        topic_title = match.group(2).strip()
        
        # Check if this is the next sequential topic
        if topic_number != last_topic_number + 1:
            logging.warning(f"Non-sequential topic number found: {chapter_number}.{topic_number}")
            continue
        
        # Check if the topic title matches any of the ignore patterns
        if ignore_regex.search(topic_title):
            logging.debug(f"Skipping unwanted topic: {chapter_number}.{topic_number} {topic_title}")
            continue
        
        # Check if the topic title contains unwanted words
        if any(word in topic_title.lower() for word in ['fig', 'figure', 'example']):
            logging.debug(f"Skipping unwanted topic: {chapter_number}.{topic_number} {topic_title}")
            continue
        
        start_pos = match.start()
        
        # Find the end of this topic (start of next topic or end of chapter)
        next_topic_pattern = rf"{chapter_number}\.{topic_number + 1}(?:\s*[:.])"
        end_pos = re.search(next_topic_pattern, chapter_data[start_pos:])
        if end_pos:
            end_pos = start_pos + end_pos.start()
        else:
            end_pos = len(chapter_data)
        
        topic_content = chapter_data[start_pos:end_pos].strip()
        
        # Remove any content after the first newline in the topic title
        first_newline = topic_content.find('\n')
        if first_newline != -1:
            topic_title = topic_content[:first_newline].strip()
            topic_content = topic_content[first_newline:].strip()
        
        chunk_data = {
            'topic': f"{chapter_number}.{topic_number} {topic_title}",
            'data': topic_content
        }
        chunks.append(chunk_data)
        logging.debug(f"Found valid topic: {chunk_data['topic']}")
        
        last_topic_number = topic_number
    
    return chunks

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
    pdf_path = "Physics_2.pdf"
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