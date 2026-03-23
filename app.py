import streamlit as st
import os
import shutil
from ingestion import run_ingestion
from brain import Brain

st.set_page_config(page_title="PDF Chat RAG", layout="wide")

DOCS_DIR = "docs"
VECTOR_DB = "chroma_db"

if "messages" not in st.session_state: st.session_state.messages = []

if "brain" not in st.session_state: st.session_state.brain = None

def save_uploaded_file(uploaded_file):
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    
    #Necessario adicionar função para limpar os arquivos anteriores.
    for filename in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e: st.error(f"Erro ao limpar: {e}") #Vendo se eu não estou ficando maluco

    file_path = os.path.join(DOCS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def reset_chat():
    st.session_state.messages = []
    if os.path.exists(VECTOR_DB):
        try:
            shutil.rmtree(VECTOR_DB)
        except: pass
    st.session_state.brain = None

#Interface
st.title("Questionarios sobre os seus PDFs")
st.markdown("Faça upload de um documento e pergunte qualquer coisa sobre ele.")

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Escolha um PDF", type="pdf")
    
    if uploaded_file and st.button("Processar Documento"):
        with st.spinner("Lendo e indexando o PDF..."):
            reset_chat()
            save_uploaded_file(uploaded_file)
            success = run_ingestion()
            if success:
                st.session_state.brain = Brain()
                st.success("Pronto! Pode começar a perguntar.")
            else:
                st.error("Falha ao processar o documento.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre o documento..."):
    if not st.session_state.brain:
        st.warning("Por favor, faça upload e processe um documento primeiro.")
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Pensando..."):
            response = st.session_state.brain.ask(prompt)
            answer_text = response["answer"]
            st.chat_message("assistant").markdown(answer_text)
            st.session_state.messages.append({"role": "assistant", "content": answer_text})
