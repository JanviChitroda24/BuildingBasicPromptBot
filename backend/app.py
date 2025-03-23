import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import random
import regex as re

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
    max_tokens=480,
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
    query_history: str

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
    "goodbye": ["bye", "goodbye", "see you", "farewell", "later", "adios", "ciao", "catch you later", "peace out"],
    "workout_plan": [
        "exercise", "gym", "bodybuilding", "weights", "lifting", "calisthenics", "yoga",
        "pilates", "crossfit", "HIIT", "running", "jogging", "workout", "cardio",
        "strength training", "resistance", "training session", "sweat", "endurance",
        "sprints", "plyometrics", "interval training", "circuit training", "aerobics", 
        "powerlifting", "bodyweight exercises", "stretching", "warm-up", "cool-down",
        "mobility", "functional training", "endurance workout", "dynamic stretching", "stability training"
    ],
    "nutrition_advice": [
        "diet", "calories", "macros", "meal plan", "vegan", "keto", "paleo", "nutrition",
        "food", "healthy eating", "balanced diet", "meal prep", "snacks", "nutritious",
        "calorie counting", "whole foods", "micronutrients", "meal timing", "intermittent fasting", "portion control",
        "fiber-rich", "lean proteins", "complex carbs", "omega-3", "antioxidants",
        "nutrient-dense", "plant-based", "gut health", "food groups", "vitamin-rich"
    ],
    "skincare": [
        "skincare", "moisturizer", "sunscreen", "acne", "pimples", "serum", "cleanser",
        "toner", "exfoliation", "anti-aging", "blemishes", "blackheads", "pores", "dark spots",
        "skin", "face wash", "mask", "hydration", "spf", "sunblock", "beauty routine", "dermatologist",
        "exfoliator", "retinol", "peptides", "anti-inflammatory", "oil-free",
        "non-comedogenic", "hydrating", "antioxidant-rich", "blemish control", "pore minimizing",
        "serum application", "hydration boost", "face moisturizer", "facial cleanser", "skin barrier"
    ],
    "common": [
        "fitness", "training", "healthy", "hydration", "weight loss", "metabolism", "protein",
        "carbs", "fat", "minerals", "vitamins", "fiber", "superfoods", "strength", "stamina",
        "health", "wellness", "lifestyle", "balance", "self care", "routine", "prevention",
        "vitality", "energy", "mindfulness", "exercise recovery", "active lifestyle", 
        "stress management", "sleep quality", "self-improvement", "routine building", "balance training",
        "daily habits", "lifestyle change", "fitness journey", "workout recovery", "health optimization"
    ]
}



@app.get("/")
async def read_root():
    return {"message": "Welcome to FitAura Bot!"}

# Intent recognition function
def recognize_intent(user_input: str):
    user_input = user_input.lower()  # Lowercase for consistency
    
    # First, check priority intents
    priority_intents = ["workout_plan", "nutrition_advice", "skincare"]
    for intent in priority_intents:
        for keyword in intent_keywords[intent]:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, user_input):
                return intent
    
    # Then check fallback intents (common, greeting, goodbye)
    fallback_intents = ["common", "greeting", "goodbye"]
    for intent in fallback_intents:
        for keyword in intent_keywords[intent]:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, user_input):
                return intent  # Return "common" if any fallback matches

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

        query_response = "Current Question: "+ request.query + "\n"+"Previous Questions: " + request.query_history
        print("Query:", query_response)

        # Invoke Gemini model
        messages = [
            ("system", system_message),
            ("human", query_response),
        ]
        response = llm.invoke(messages)

        # Return JSON response
        return {"query": request.query, "intent_response": intent_response, "response": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
