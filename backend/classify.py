from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os

llm = ChatGroq(
    model="Gemma2-9b-It",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def classify_document_type(text: str):
    doc_type_prompt = f"What type of document is this? Choose one: Bill of Exchange, GRN, PO.\n\nText:\n{text}"
    response = llm([HumanMessage(content=doc_type_prompt)])
    return response.content.strip()
