from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
import json

llm = ChatGroq(
    model="Gemma2-9b-It",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

prompt_template = """
You are an intelligent document parser. Extract key-value pairs from the given text.

Extract both:
1. Standard fields (e.g., Drawer, Drawee, PO Number, etc.)
2. Any additional new fields found in the document.

Respond only with a JSON object. Input Text:
{text}
"""

def extract_fields_from_text(text: str):
    prompt = prompt_template.format(text=text)
    response = llm([HumanMessage(content=prompt)])
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:", response.content)
        return {"error": "Invalid JSON format", "raw_response": response.content}
