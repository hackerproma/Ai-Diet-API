import os
from google import genai
from google.genai import types

# Load API Key safely from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def analyze_food(image):
    if not image:
        return {"error": "No image provided"}

    if not GOOGLE_API_KEY:
        return {"error": "GOOGLE_API_KEY environment variable is not set"}

    # Initialize Client
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Read image binary data and grab mime-type (defaults to image/jpeg)
    image_bytes = image.read()
    mime_type = getattr(image, "content_type", "image/jpeg")

    prompt = (
        "You are a clinical nutritionist. Identify the food in the image, estimate the "
        "average calories, and determine the meal_type (breakfast, lunch, snack, or dinner) "
        "based on standard consumption patterns."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are a clinical nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "food_name": {"type": "STRING"},
                        "average_calorie": {"type": "NUMBER"},
                        "meal_type": {"type": "STRING"},
                    },
                    "required": ["food_name", "average_calorie", "meal_type"],
                },
            ),
        )

        # Automatically parsed output dictionary when response_mime_type is JSON
        return response.parsed

    except Exception as e:
        return {"error": str(e)}


def generate_kerala_diet_plan(goal="weight loss", age=None, weight=None, gender="male", target_weight=None, duration=None):
    if not GOOGLE_API_KEY:
        return {"error": "GOOGLE_API_KEY environment variable is not set"}

    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    prompt = (
        f"Create a Kerala-style {goal} diet plan. "
        f"User: {gender}, {age}yrs, {weight}kg. "
        f"Target: {target_weight}kg in {duration} months."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Kerala Nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "daily_calories": {"type": "NUMBER"},
                        "diet_plan": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "day": {"type": "STRING"},
                                    "meals": {
                                        "type": "ARRAY",
                                        "items": {"type": "STRING"}
                                    }
                                }
                            }
                        }
                    }
                }
            )
        )
        
        return response.parsed
        
    except Exception as e:
        return {"error": str(e)}