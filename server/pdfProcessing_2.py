import pdfplumber
import re
import json
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"Extracting text from {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        
        # text = clean_extracted_text(text)
        print(f"Extracted and cleaned text (first 500 chars): {text[:500]}")
        
        with open("Physics.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise

def split_into_chapters(text: str) -> List[Dict[str, str]]:
    print("Splitting text into chapters")
    chapter_pattern = r"(Chapter \w+)\s*\n([A-Z][A-Z\s]+)"
    matches = list(re.finditer(chapter_pattern, text, re.MULTILINE))
    print(f"Number of chapter matches found: {len(matches)}")
    
    if not matches:
        print("No chapters found in the text.")
        print(f"Text snippet (first 1000 chars):\n{text[:1000]}")
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
        print(f"Found chapter: {chapter_data['chapter']} - {chapter_data['title']}")
    
    return chapters

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

def chunk_chapter_by_topics(chapter_data: str, chapter_number: int) -> List[Dict[str, str]]:
    print(f"Chunking chapter {chapter_number} by topics")
    topic_pattern = rf"(?<!Fig\.\s)(?<!Figure:\s)^{chapter_number}\.(\d+)(?:\s*[:.]?)\s+([A-Z][A-Za-z\s]+)"
    matches = list(re.finditer(topic_pattern, chapter_data, re.MULTILINE))
    print(f"Number of potential topic matches found: {len(matches)}")
    
    if not matches:
        print(f"No topics found in Chapter {chapter_number}.")
        return [{'topic': 'Untitled', 'data': chapter_data.strip()}]

    chunks = []
    last_topic_number = 0

    for match in matches:
        topic_number = int(match.group(1))
        topic_title = match.group(2).strip()

        if re.match(r'^\d+$', topic_title) or re.match(r'^\(\d+\)$', topic_title):
            continue

        if topic_number != last_topic_number + 1:
            print(f"Non-sequential topic number found: {chapter_number}.{topic_number}")
            continue

        start_pos = match.start()
        next_topic_pattern = rf"^{chapter_number}\.{topic_number + 1}\s+"
        end_pos = re.search(next_topic_pattern, chapter_data[start_pos:], re.MULTILINE)
        if end_pos:
            end_pos = start_pos + end_pos.start()
        else:
            end_pos = len(chapter_data)

        topic_content = chapter_data[start_pos:end_pos].strip()
        topic_content = convert_math_to_markdown(topic_content)

        chunk_data = {
            'topic': f"{chapter_number}.{topic_number} {topic_title}",
            'data': topic_content
        }
        chunks.append(chunk_data)
        last_topic_number = topic_number
        print(f"Added topic: {chunk_data['topic']}")

    return chunks

def process_and_chunk_pdf(pdf_path: str, output_file: str) -> None:
    try:
        pdf_text = extract_text_from_pdf(pdf_path)
        chapters = split_into_chapters(pdf_text)
        
        if not chapters:
            print("No chapters found. Cannot proceed with processing.")
            return

        for i, chapter in enumerate(chapters, 1):
            chapter['chunks'] = chunk_chapter_by_topics(chapter['data'], i)
            del chapter['data']
        
        save_to_json(chapters, output_file)
        print(f"Successfully processed PDF and saved results to {output_file}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise

def save_to_json(data: List[Dict], output_file: str) -> None:
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        raise

if __name__ == "__main__":
    pdf_path = "Physics.pdf"
    output_file = "chunked_physics_data_2.json"

    process_and_chunk_pdf(pdf_path, output_file)

    try:
        with open(output_file, 'r') as f:
            chunked_data = json.load(f)
        if chunked_data and chunked_data[0].get('chunks'):
            print(json.dumps(chunked_data[0]['chunks'][0], indent=4))
        else:
            print("No chunks found in the first chapter.")
    except Exception as e:
        print(f"Error reading or displaying sample chunk: {e}")