import os
import getpass
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# 1️⃣ Load environment variables from .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

# 2️⃣ Set the Google AI API key correctly
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")  # Make sure .env contains GEMINI_API_KEY

if GOOGLE_API_KEY is None:
    raise ValueError("GEMINI_API_KEY is not found. Please set it in the .env file.")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY  # Ensure the API key is available globally

# 3️⃣ Instantiate the Google Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Choose model version
    temperature=0.7,  # Adjust creativity level
    max_tokens=512,  # Set output token limit
    timeout=30,  # Request timeout in seconds
    max_retries=2,  # Number of retries on failure
)

# 4️⃣ Define messages (system & user)
messages = [
    ("system", "You are a helpful assistant that translates English to French."),
    ("human", "I love programming."),
]

# 5️⃣ Invoke the model and get a response
response = llm.invoke(messages)

# 6️⃣ Print the output
print("AI Response:", response.content)
