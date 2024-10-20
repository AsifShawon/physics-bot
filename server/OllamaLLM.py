from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from pdfToVectoreStore import search
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Global variables
chatHistory = []
systemMessage = """You are a helpful physics assistant, committed to delivering clear and accurate explanations. Always accompany your explanations with relevant examples, either from the provided physics book or generated by yourself.

For questions outside the domain of physics, respond with: I can assist only with physics-related queries.

You will be given additional context to guide your responses. Focus strictly on physics and avoid answering unrelated questions."""

chatHistory.append(SystemMessage(content=systemMessage))

# Initialize the Ollama model
ollama_model = Ollama(model="gemma2:2b-instruct-q4_K_M")
prev_query = ""
prev_reply = ""

def vectorise_text(texts):
    if isinstance(texts, str):
        texts = [texts]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    return vectors

def get_cosine_similarity(query, text):
    combined_texts = [query, text]
    vectors = vectorise_text(combined_texts)
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:2])
    print(cosine_similarities[0][0])
    return cosine_similarities[0][0]

def generate_text(query):
    global prev_query, prev_reply

    # Define different prompt templates
    general_prompt = """Question: {query}

    Context: {context}

    Please provide a clear and concise answer to the question, focusing on physics concepts. If possible, include a relevant example from the provided context or a well-known physics principle."""

    calculation_prompt = """Question: {query}

    Context: {context}

    This question requires a calculation. Please follow these steps:
    1. Identify the relevant physics formula(s) needed to solve the problem.
    2. List the given values and what needs to be calculated.
    3. Show the step-by-step calculation process.
    4. Provide the final answer with the correct units."""

    conceptual_prompt = """Question: {query}

    Context: {context}

    This question is about a physics concept. Please structure your response as follows:
    - Define the concept clearly."""

    follow_up_prompt = """Follow-up Request: {query}

    Based on the previous discussion, please address this follow-up request. If it's asking for:
    - More details: Expand on the most relevant aspect of the previous explanation.
    - An example: Provide a concrete example that illustrates the concept discussed.

    Remember to maintain focus on physics concepts and their applications."""

    # Check if it's a follow-up question
    follow_up_keywords = [
    'tell me more', 'describe', 'give an example', 'explain further', 'clarify',
    'can you elaborate', 'more details', 'expand on', 'what about', 'how about',
    'could you explain', 'could you describe', 'can you provide', 'can you give',
    'please explain', 'please describe', 'please provide', 'please give',
    'follow up', 'additional information', 'more information', 'further details'
    ]
    
    is_follow_up = any(keyword in query.lower() for keyword in follow_up_keywords) or \
                   (prev_query and get_cosine_similarity(query, prev_query) >= 0.5) or \
                   (prev_reply and get_cosine_similarity(query, prev_reply) >= 0.5)

    if is_follow_up:
        selected_prompt = follow_up_prompt
        context = "This is a follow-up to the previous discussion. No new context is provided."
    else:
        # Retrieve context from physics documents for new questions
        retrieved_text = search(query)

        # Determine which prompt to use based on the query
        if any(keyword in query.lower() for keyword in ['calculate', 'solve', 'find the value']):
            selected_prompt = calculation_prompt
        elif any(keyword in query.lower() for keyword in ['what is', 'define', 'explain']):
            selected_prompt = conceptual_prompt
        else:
            selected_prompt = general_prompt

        # Check if relevant content was found
        if retrieved_text != "No relevant docs were retrieved using the relevance score threshold 0.5":
            context = f"Here are some documents that might help answer the question: \n{retrieved_text}"
        else:
            context = "Unfortunately, I couldn't find any relevant documents. I'll answer based on my general knowledge of physics."

    # Create the full prompt
    full_prompt = selected_prompt.format(query=query, context=context)
    chatHistory.append(HumanMessage(content=full_prompt))
    
    # Generate response from the model
    try:
        response = ollama_model.invoke(full_prompt)  # Correct method for model invocation
        response = StrOutputParser().parse(response) 
        prev_query = query
        prev_reply = response
    except Exception as e:
        return f"Error generating response: {e}"

    chatHistory.append(AIMessage(content=response))
    return response

# To clear chat history for a new session
def clear_chat_history():
    global prev_query, prev_reply
    chatHistory.clear()
    chatHistory.append(SystemMessage(content=systemMessage))
    prev_query = ""
    prev_reply = ""