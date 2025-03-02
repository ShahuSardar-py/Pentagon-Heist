import os
from dotenv import load_dotenv
from google import genai
import json
import random

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)
def AIresponse(prompt):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt])

    return response




def generate_intro():

    prompt = (
        "Create a thrilling heist introduction that:\n"
        "1. Sets the scene at the Pentagon.\n"
        "2. Mentions one specific security measure.\n"
        "3. Hints at a potential weakness.\n"
        "Keep it under 100 words with dramatic flair.\n\n"
        "Example:\n"
        "\"The Pentagon's Quantum Encryption Vault glows ominously. Rumors whisper of a legacy system vulnerability that might be exploited...\""
    )
    # Get the AI response (a string)
    intro = AIresponse(prompt)
    return intro

def get_challenge(attempt, intro_context):

    prompt = (
        f"Based on the following heist introduction:\n"
        f"{intro_context}\n\n"
        f"Create security challenge #{attempt} with the following requirements:\n"
        "1. Provide a description that references a specific security measure at the Pentagon mentioned or hinted at in the introduction.\n"
        "2. Give 3 tool options (one correct, two decoys).\n"
        "3. Specify the correct option explicitly.\n"
        "4. Describe a failure consequence if the wrong option is chosen.\n"
        "5. Provide a code value as 'Code' (ex: TURBO-PENGUIN-921) that ties into the overall heist theme.\n"
        "6. Include a subtle hint that relates to the introduction.\n\n"
        "Format the output as JSON, for example:\n"
        "{\n"
        "  \"description\": \"...\",\n"
        "  \"options\": [\"...\", \"...\", \"...\"],\n"
        "  \"correct\": \"...\",\n"
        "  \"failure\": \"...\",\n"
        "  \"Code\": \"...\",\n"
        "  \"hint\": \"...\"\n"
        "}"
    )
    try:
        # Get the AI-generated challenge as a string and parse it as JSON.
        response = AIresponse(prompt)
        challenge = json.loads(response)
        
        # Randomize the order of options while ensuring the correct option remains present.
        options = challenge.get("options", [])
        correct = challenge.get("correct")
        if options:
            random.shuffle(options)
            if correct not in options:
                
                options[0] = correct
            challenge["options"] = options
        
        return challenge
    except Exception as e:
        # In case of any error, return a fallback challenge.
        fallback_challenge = {
            "description": "A holographic security guard materializes, scanning for intruders reminiscent of the clues in your introduction.",
            "options": ["Use a cloaking device", "Hack its sensor", "Distract with a noise"],
            "correct": "Hack its sensor",
            "failure": "The hologram alerts the real security team!",
            "Code": "HALO",  # Predefined code value
            "hint": "Remember, the guard's sensors have a blind spot hinted in the intro."
        }
        return fallback_challenge



