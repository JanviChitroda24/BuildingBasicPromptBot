import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import random

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

intent_responses = {
    "greeting": ["Hello! How can I help you?", "Hi there! What do you need assistance with?"],
    "goodbye": ["Goodbye! Have a great day!", "See you soon! Take care."],
    "workout_plan": ["I can suggest a workout plan. What’s your fitness goal?"],
    "nutrition_advice": ["Healthy eating is essential! Do you have any dietary preferences?"],
    "skincare": ["Skincare routine is essential! Do you want to build a skincare routine?"],
    "default": ["I’m not sure I understand. Can you rephrase?"]
}

intent_keywords = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "what's up", "howdy", "yo"],
    "goodbye": ["bye", "goodbye", "see you", "farewell", "take care", "later", "adios", "ciao", "catch you later", "peace out"],
    "workout_plan": [
        "workout", "exercise", "gym", "fitness", "training", "bodybuilding", "cardio", "weights", "lifting", "aerobics",
        "strength", "calisthenics", "yoga", "pilates", "crossfit", "endurance", "stamina", "HIIT", "running", "jogging"
    ],
    "nutrition_advice": [
        "diet", "nutrition", "food", "calories", "protein", "carbs", "fat", "macros", "meal plan", "healthy eating",
        "fiber", "vitamins", "minerals", "hydration", "superfoods", "weight loss", "metabolism", "vegan", "keto", "paleo"
    ],
    "skincare": [
        "skincare", "skin", "moisturizer", "sunscreen", "acne", "pimples", "serum", "cleanser", "toner", "hydration",
        "exfoliation", "anti-aging", "blemishes", "blackheads", "pores", "oily skin", "dry skin", "sensitive skin", "glowing skin", "dark spots"
    ]
}


@app.get("/")
async def read_root():
    return {"message": "Welcome to FitAura Bot!"}

# Intent recognition function
def recognize_intent(user_input: str):
    user_input = user_input.lower()
    for intent, keywords in intent_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return intent
    return ""

# API Endpoint for sending message to AI model
@app.post("/send_message")
async def translate_text(request: QueryRequest):
    try:
        # Define messages for translation
        messages = [
            ("system", f"You are a skincare expert. Can you help a {request.gender} who is a {request.age} years old."),
            ("human", request.query),
        ]

        intent = recognize_intent(request.query)
        # Recognize intent
        intent = recognize_intent(request.query)
        print("Intent ",intent)
        # Check if intent exists and then choose a response
        if intent and intent in intent_responses:
            intent_response = random.choice(intent_responses[intent])
        else:
            intent_response = ""

        print("Intent Response ",intent_response)

        # Invoke Gemini model
        response = llm.invoke(messages)

        # Return JSON response
        return {"query":request.query, "intent_response":intent_response, "response": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

