import streamlit as st
from OllamaLLM import generate_text

st.title("Physics Chatbot",anchor=False)
model = st.sidebar.selectbox("Select Model",["llama3.1","gemma2:2b"])  

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(generate_text(model,text))
    # st.info("HEllo")