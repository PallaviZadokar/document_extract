import streamlit as st
import requests

st.set_page_config(page_title="Document Data Extractor")
st.title(" Document Data Extractor")

uploaded_file = st.file_uploader("Upload a document ", type=["pdf", "docx", "jpg", "jpeg", "png"])

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
            st.success("Data extracted successfully!")

            
            st.markdown(f" Document Type: `{result['document_type']}`")

            data = result.get("extracted_data", {})
            
            if "error" in data:
                st.error("Failed to parse structured fields.")
                st.subheader("Raw Output:")
                st.code(data["raw_response"], language="json")
            else:
                standard_fields = data.get("standard_fields", {})
                additional_fields = data.get("additional_fields", {})

                st.subheader("Standard Fields:")
                for key, value in standard_fields.items():
                    st.write(f"**{key}:** {value}")

                if additional_fields:
                    st.subheader("Additional Fields:")
                    for key, value in additional_fields.items():
                        st.write(f"**{key}:** {value}")
                else:
                    st.info("No additional fields found.")

        except Exception as e:
            st.error(f"Extraction failed: {e}")
