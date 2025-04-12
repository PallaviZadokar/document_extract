import re 
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
import json

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

prompt_template = """
You are an intelligent document parser. Extract key-value pairs from the given text.

Extract both:
1. Standard fields (e.g., Drawer, Drawee, Supplier Name, GRN Number, PO Number, Buyer Name, etc.)
2. Any additional new fields found in the document.

Respond only with a JSON object. Input Text:
{text}
"""


def extract_fields_from_text(text: str):
    prompt = prompt_template.format(text=text)
    response = llm([HumanMessage(content=prompt)])
    
    
    cleaned = re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", response.content, flags=re.DOTALL)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("Failed to parse JSON. Raw output:", response.content)
        return {"error": "Invalid JSON format", "raw_response": response.content}
