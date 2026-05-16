from tavily import TavilyClient
import os 
from dotenv import load_dotenv
load_dotenv()
def search_tavily(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    output = ""
    for result in response["results"]:
        output += f"{result['title']}\n{result['content']}\n---\n"
    return output
        
def calculate(expression):
    result = eval(expression)
    return f"The result of {expression} is: {result}"
    
def load_document(file_path: str):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(splits, embeddings, persist_directory="./chroma_db")
    
    return vector_store

def search_document(query: str, vector_store) -> str:
    retrieved_docs = vector_store.similarity_search(query, k=3)
    if not retrieved_docs:
        return "No relevant information found in document."
    return "\n\n".join(doc.page_content for doc in retrieved_docs)
