import streamlit as st
import requests

st.title("Document Data Extractor")

uploaded_file = st.file_uploader("Upload a document (PDF or Word)", type=["pdf", "docx"])

if uploaded_file:
    st.info("Extracting data from document...")

   
    with open("temp_uploaded_file", "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open("temp_uploaded_file", "rb") as f:
        files = {"file": (uploaded_file.name, f, uploaded_file.type)}
        try:
            response = requests.post("http://localhost:8000/extract", files=files)
            response.raise_for_status()
            result = response.json()
            st.success("Data extracted!")
            st.json(result["extracted_data"])
        except Exception as e:
            st.error(f"Extraction failed: {e}")

