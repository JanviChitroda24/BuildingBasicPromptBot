import os
from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Google Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

# Define API route for text generation
@app.post("/generate/")
async def generate_text(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return {"response": response.text if response and response.text else "No response received."}
    except Exception as e:
        return {"error": str(e)}

# Run the server using: uvicorn main:app --reload
