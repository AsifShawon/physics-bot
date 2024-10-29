import json
import time
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search

class PhysicsQAGenerator:
    def __init__(self, api_key: str, input_file: str):
        self.api_key = api_key  # Store API key separately
        self.input_file = input_file
        self.system_message = """You are a helpful physics assistant, committed to delivering clear and accurate explanations. Always accompany your explanations with relevant examples, either from the provided physics book or generated by yourself.

For questions outside the domain of physics, respond with: I can assist only with physics-related queries.

You will be given additional context to guide your responses. Focus strictly on physics and avoid answering unrelated questions."""
        self.reset_llm()
        
    def reset_llm(self):
        """Reset the LLM instance to clear conversation history"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=self.api_key
        )
        print("\nReset chat history")
        
    def load_json(self) -> List:
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, data: List):
        with open(self.input_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def generate_prompt(self, question: str, is_follow_up: bool = False) -> str:
        context = search(question)
        
        if is_follow_up:
            prompt_template = """Follow-up Question: {question}

Context: {context}

Please provide a detailed answer that:
1. Directly addresses the follow-up question
2. Builds upon the main concept
3. Includes specific examples where appropriate
4. Maintains clear connection to physics principles"""
        else:
            prompt_template = """Question: {question}

Context: {context}

Please provide a comprehensive answer that:
1. Defines any key terms
2. Explains the core physics concepts involved
3. Includes relevant examples
4. Uses clear, precise language
5. Maintains scientific accuracy"""

        return prompt_template.format(question=question, context=context)

    def generate_answer(self, question: str, is_follow_up: bool = False) -> str:
        prompt = self.generate_prompt(question, is_follow_up)
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error generating answer for question: {question}")
            print(f"Error: {e}")
            return ""

    def process_question_set(self, question_set: Dict):
        # Process main question if it doesn't have an answer
        if not question_set["main_question"].get("a"):
            print(f"Processing question: {question_set['main_question']['q']}")
            answer = self.generate_answer(question_set["main_question"]["q"])
            question_set["main_question"]["a"] = answer
            print(f"Answer: {answer}")  # Print the answer after generating it
            time.sleep(1)  # Rate limiting

        # Process follow-up questions if they exist and don't have answers
        if "follow_up_questions" in question_set:
            for follow_up in question_set["follow_up_questions"]:
                if not follow_up.get("a"):
                    print(f"Processing follow-up: {follow_up['q']}")
                    answer = self.generate_answer(follow_up["q"], is_follow_up=True)
                    follow_up["a"] = answer
                    print(f"Follow-up Answer: {answer}")  # Print the follow-up answer after generating it
                    time.sleep(1)  # Rate limiting


    def process_all_questions(self):
        data = self.load_json()
        total_chapters = len(data)
        
        for chapter_idx, chapter in enumerate(data, 1):
            print(f"\nProcessing Chapter {chapter_idx}/{total_chapters}: {chapter['chapter']}")
            # print("hello")
            
            for topic in chapter["topics"]:
                print(f"\nTopic: {topic['topic']}")
                
                for type_section in topic["types"]:
                    print(f"Type: {type_section['type']}")
                    
                    for question_set in type_section["questions"]:
                        self.process_question_set(question_set)
                        # Save after each question set to prevent data loss
                        self.save_json(data)
                    
                    # Reset LLM after completing each type section
                    self.reset_llm()
                        
            print(f"Completed Chapter {chapter_idx}: {chapter['chapter']}")

def main():
    GOOGLE_API_KEY = "AIzaSyAfBDLnOerYntiLjmwA0PmJ-yZmN5LvCJ0"
    input_file = "output3.json"
    
    try:
        generator = PhysicsQAGenerator(GOOGLE_API_KEY, input_file)
        generator.process_all_questions()
        print("\nProcessing completed successfully!")
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user. Progress has been saved.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()