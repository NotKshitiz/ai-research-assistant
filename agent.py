from time import time

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv
from tools import search_tavily, calculate, load_document, search_document
from langchain_core.messages import SystemMessage
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")                           # Keeps your agent's tools stable
)

@tool
def web_search(query:str)->str:
    """Search the web for current news, recent events, and general information."""
    return search_tavily(query)
@tool
def calculator(expression:str)->str:
    """Calculate a mathematical expression like '15 * 27' or '100 / 4'."""
    return calculate(expression)

vector_store = None
@tool
def document_search(query: str) -> str:
    """Search the uploaded document for specific information."""
    if vector_store is None:
        return "No document uploaded yet."
    return search_document(query, vector_store)

agent = create_react_agent(llm,tools=[web_search,calculator,document_search],prompt=SystemMessage(content="You are an expert research assistant. When tools return information, "
        "your job is to ruthlessly filter out any noise, boilerplate text, or "
        "irrelevant data. Provide only a concise, highly relevant summary of "
        "the actual facts the user asked for."))
