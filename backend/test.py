import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Google Gemini API client
genai.configure(api_key=GEMINI_API_KEY)

# Select the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("Explain how AI works in a 500 words")

# Print response
if response and response.text:
    print("Success!")
    print(response.text)
else:
    print("No response received.")
