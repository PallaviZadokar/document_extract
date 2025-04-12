from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def classify_document_type(text: str):
    doc_type_prompt = f"What type of document is this? Choose one: Bill of Exchange, Goods Receipt Note, Purchase Order.\n\nText:\n{text}"
    response = llm([HumanMessage(content=doc_type_prompt)])
    return response.content.strip()
