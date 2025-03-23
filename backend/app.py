import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

# Set up Google AI API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if GOOGLE_API_KEY is None:
    raise ValueError("GEMINI_API_KEY is not found. Please set it in the .env file.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY  # Ensure API key is available globally

# Instantiate FastAPI app
app = FastAPI(title="AI Translation API", version="1.0")

# Instantiate Google Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    max_tokens=512,
    timeout=30,
    max_retries=2,
)

# Define request model
class QueryRequest(BaseModel):
    query: str 
    name: str
    email: str
    age: int
    gender: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to FitAura Bot!"}

# API Endpoint for Translation
@app.post("/send_message")
async def translate_text(request: QueryRequest):
    try:
        # Define messages for translation
        messages = [
            ("system", f"You are a skincare expert. Can you help a {request.gender} who is a {request.age} years old."),
            ("human", request.query),
        ]

        # Invoke Gemini model
        response = llm.invoke(messages)

        # Return JSON response
        return {"message": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

