import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import pinecone 
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Get API keys securely
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found. Check your .env file.")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

# Load PDF data
def load_pdf_file(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

# Provide your PDF file path
pdf_path = "C:/Bits_hyd/doctor_pov/CuraMateDR/Data/tb.pdf"
extracted_data = load_pdf_file(pdf_path)

# Split text into smaller chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = text_split(extracted_data)

# Load embeddings
def get_hugging_face_embedding():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

embeddings = get_hugging_face_embedding()

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY, environment="us-east-1")

# Connect to the existing index
index_name = "medibot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name, 
    embedding=embeddings
)

# Create retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Function to retrieve relevant text from Pinecone
def retrieve_text(question):
    retrieved_docs = retriever.invoke(question)
    retrieved_texts = [doc.page_content for doc in retrieved_docs]
    return "\n".join(retrieved_texts)

# Function to generate AI-powered response using Gemini
def generate_response(question):
    context = retrieve_text(question)
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
    You are a medical assistant. Use the following retrieved context to answer the question accurately.
    
    Context:
    {context}

    Question: {question}
    
    Provide a detailed and precise medical response.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Example query
query = "What are the symptoms of tuberculosis?"
response = generate_response(query)
print("Final AI Response:", response)
