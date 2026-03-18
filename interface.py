import streamlit as st
import requests
import os
# Set the FastAPI endpoint URLs
BASE_URL = "https://2kbqwmz42s.us-east-1.awsapprunner.com"
UPLOAD_URL = f"{BASE_URL}/upload"
ASK_URL = f"{BASE_URL}/ask"
SAMPLE_DIR = "."

st.set_page_config(page_title="Feed your RAG and talk to it", layout='wide')


st.title("🤖 SimkoRAG Custom RAG agent")
st.markdown("Upload your PDFs to train the agent, then ask questions based on the content.")

with st.sidebar:
    st.header("Document training")

    upload_file = st.file_uploader("Upload a PDF", type = "pdf")

    if st.button("Process & train"):
        if upload_file is not None:
            with st.spinner("Processing PDF"):

                files = {"file": (upload_file.name, upload_file.getvalue(), "application/pdf")}

                try:
                    response = requests.post(UPLOAD_URL, files = files)
                    if response.status_code == 200:
                        st.success(f"Succesfully indexed: {upload_file.name}")
                        st.json(response.json())
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"connection failed: {e}")
        else:
            st.warning("Please select a file first")

st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input("Ask somethign about your document: "):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    

    with st.chat_message("assistant"):
        with st.spinner("Thinking.... sagbab"):
            try:
                response = requests.post(ASK_URL, json = {"prompt": prompt})
                if response.status_code == 200:
                    answer = response.json().get("answer", "answer not found")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("The agent encountered an error while processing your request...")
            except Exception as e:
                st.errro(f"failed to connect to the backend {e}")

