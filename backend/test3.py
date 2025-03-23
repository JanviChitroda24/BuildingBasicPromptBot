import regex as re

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

# Intent recognition function
import re

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


if __name__ == "__main__":
    # Test cases for the recognize_intent function

    test_inputs = [
        "Hello there, how are you?",                       # greeting
        "I want to hit the meal timing",         # workout_plan
        "What's a good diet to follow for weight loss?",     # nutrition_advice
        "My skin has been acting up, any tips on moisturizers?",  # skincare
        "I'm looking to improve my overall health and wellness.", # common
        "I love reading books."                             # default (no matching keywords)
    ]

    for text in test_inputs:
        intent = recognize_intent(text)
        print(f"Input: {text}\nRecognized intent: {intent}\n")
