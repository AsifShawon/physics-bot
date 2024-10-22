import streamlit as st
import time
from st_chat_message import message as stcm
from OllamaLLM import generate_text, clear_chat_history

# Configure Streamlit page
st.set_page_config(
    page_title="Physics Chatbot",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stSpinner {
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Physics Chatbot 🔬", anchor=False)

# Sidebar configuration
with st.sidebar:
    st.header('Welcome! 👋', divider="red")
    model = "gemma2:2b-instruct-q4_K_M"
    st.subheader(f"Model: :red[{model}]", divider="gray")
    
    # New chat button with session state management
    if st.button("New Chat 🔄"):
        st.session_state.messages = []
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your physics assistant. How can I help you today?"}]
        clear_chat_history()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your physics assistant. How can I help you today?"}]

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        stcm(message["content"], is_user=True, avatar_style="adventurer")
    else:
        stcm(message["content"], avatar_style="bottts")

# Chat input and response generation
if prompt := st.chat_input("Ask me anything about physics..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    stcm(prompt, is_user=True, avatar_style="adventurer")

    # Generate and display assistant response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("🤔 Thinking..."):
            try:
                start_time = time.time()
                response = generate_text(prompt)
                end_time = time.time()
                print(f"Response time: {(end_time - start_time):.2f} seconds")
                
                # Display response
                stcm(response, avatar_style="bottts")
                
                # Add to session state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display response time in sidebar
                with st.sidebar:
                    st.caption(f"Response time: {(end_time - start_time):.2f} seconds")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I apologize, but I encountered an error. Please try again."
                })