import streamlit as st
import time
from st_chat_message import message as stcm
from OllamaLLM import generate_text, clear_chat_history

st.title("Physics Chatbot", anchor=False)

with st.sidebar:
    st.header('Welcome !', divider="red")
    # model = st.selectbox("Select a model", ["llama3.2:3b", "gemma2:9b", "gemma2:2b", "qwen2.5:3b"])
    model = "gemma2:2b-instruct-q4_K_M"
    # model = "llama3.2:3b-instruct-q4_K_M"
    st.subheader(f"Model we are using: :red[{model}]", divider="gray")
    button = st.button("New Chat")
    if button:
        st.session_state.clear()
        clear_chat_history()

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
for message in st.session_state.messages:
    if message["role"] == "user":
        stcm(message["content"], is_user=True, avatar_style="adventurer")
    else:
        stcm(message["content"])
        

def generate_response(prompt):
    print(model)
    response = generate_text(prompt)
    return response


if prompt := st.chat_input("Type something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with st.chat_message("user"):
    stcm(prompt, is_user=True)

if st.session_state.messages[-1]["role"] != "assistant":
    # with st.chat_message("assistant"):
    with st.spinner("Thinking..."):

        start = time.time()
        print(f"Start: {start}")
        response = generate_response(prompt)
        end = time.time()
        print(f"End: {end}")
        print(f"Total: {end-start}")

        # placeholder = stcm("")
        full_response = ''
        for item in response:
            full_response += item
            # placeholder.markdown(full_response)
        stcm(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)