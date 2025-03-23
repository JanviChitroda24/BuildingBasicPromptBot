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
    "common": ["Could you clarify? Are you asking about skincare, exercise, or nutrition?"],
    "default": ["I’m not sure I understand. Can you rephrase?", "I am trained to only answer questions on fitness, nutrition, and skincare."]
}

intent_keywords = {
    "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "what's up"],
    "goodbye": ["bye", "goodbye", "see you", "farewell", "take care", "later", "adios", "ciao", "catch you later", "peace out"],
    "workout_plan": [
        "exercise", "gym", "bodybuilding", "weights", "lifting", "calisthenics", "yoga", "pilates", "crossfit", "HIIT", "running", "jogging", "workout", "exercise"
    ],
    "nutrition_advice": [
        "diet", "calories", "macros", "meal plan", "vegan", "keto", "paleo", "nutrition", "food"
    ],
    "skincare": [
        "skincare", "moisturizer", "sunscreen", "acne", "pimples", "serum", "cleanser", "toner", "exfoliation", "anti-aging", "blemishes", "blackheads", "pores", "dark spots"
    ],
    "common": [
        "fitness", "training", "healthy", "hydration", "weight loss", "metabolism", "protein", "carbs", "fat", "minerals", "vitamins", "fiber", "superfoods", "strength", "stamina"
    ]
}



@app.get("/")
async def read_root():
    return {"message": "Welcome to FitAura Bot!"}

# Intent recognition function
def recognize_intent(user_input: str):
    user_input = user_input.lower()
    
    # First, check all intents except "common"
    for intent, keywords in intent_keywords.items():
        if intent != "common":  # Skip "common" in this loop
            if any(keyword in user_input for keyword in keywords):
                return intent
    
    # Finally, check "common"
    if any(keyword in user_input for keyword in intent_keywords["common"]):
        return "common"
    
    return "default"


# API Endpoint for sending message to AI model
@app.post("/send_message")
async def translate_text(request: QueryRequest):
    try:
        # Recognize intent
        intent = recognize_intent(request.query)
        print("Intent:", intent)

        # If intent is greeting, goodbye, or default, return a direct response
        if intent in ["greeting", "goodbye", "default", "common"]:
            response  = random.choice(intent_responses[intent])
            if intent == "common":
                return {"query": request.query, "intent_response": "common", "response": response}
            return {"query": request.query, "intent_response": "", "response": response}

        # Define prompt based on intent
        if intent == "workout_plan":
            system_message = f"You are a certified fitness coach. Can you create a personalized workout plan for a {request.gender} who is {request.age} years old?"
        elif intent == "nutrition_advice":
            system_message = f"You are a nutrition expert. Provide dietary recommendations for a {request.gender} who is {request.age} years old."
        elif intent == "skincare":
            system_message = f"You are a dermatologist. Give skincare recommendations for a {request.gender} who is {request.age} years old."
        else:
            system_message = f"You are an expert. Can you help a {request.gender} who is {request.age} years old?"

        # Fetch a relevant intent response if available
        intent_response = random.choice(intent_responses[intent])
        print("Intent Response:", intent_response)

        # Invoke Gemini model
        messages = [
            ("system", system_message),
            ("human", request.query),
        ]
        response = llm.invoke(messages)

        # Return JSON response
        return {"query": request.query, "intent_response": intent_response, "response": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
