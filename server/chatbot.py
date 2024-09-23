import streamlit as st
import time
from OllamaLLM import generate_text, clear_chat_history

st.title("Physics Chatbot", anchor=False)

with st.sidebar:
    st.title('Welcome !')
    button = st.button("New Chat")
    model = st.selectbox("Select a model", ["llama3.1:8b", "gemma2:9b", "gemma2:2b"])
    if button:
        st.session_state.clear()
        clear_chat_history()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def generate_response(prompt):
    print(model)
    response = generate_text(model, prompt)
    return response


if prompt := st.chat_input("Type something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            start = time.time()
            print(f"Start: {start}")
            response = generate_response(prompt)
            end = time.time()
            print(f"End: {end}")
            print(f"Total: {start-end}")

            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)