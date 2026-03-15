import streamlit as st
import pandas as pd
from langchain_community.llms import Ollama
from textblob import TextBlob

# Load LLM
llm = Ollama(model="llama3")

st.title("📚 ClassGPT AI Assistant")

# Chat memory
if "history" not in st.session_state:
    st.session_state.history = []

# spelling correction function
def correct_text(text):
    words = text.split()
    corrected = []
    
    for w in words:
        if len(w) > 6:   # assume long words may be names
            corrected.append(w)
        else:
            corrected.append(str(TextBlob(w).correct()))
    
    return " ".join(corrected)

# Upload files
uploaded_file = st.file_uploader(
    "Upload CSV / Excel / TXT",
    type=["csv","xlsx","txt"]
)

knowledge = ""

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        knowledge = df.to_string()

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        knowledge = df.to_string()

    else:
        knowledge = uploaded_file.read().decode()

    st.success("File uploaded successfully!")

# Ask question
user_question = st.text_input("Ask your question")



if user_question:

    corrected = correct_text(user_question)

    prompt = f"""
    Answer using this information:

    {knowledge}

    Question: {corrected}
    """

    response = llm.invoke(prompt)

    st.session_state.history.append((corrected,response))

# Show chat history
for q,a in st.session_state.history:
    st.write("🧑:",q)
    st.write("🤖:",a)