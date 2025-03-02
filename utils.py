import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import random

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Configure the API (this is the correct initialization)
genai.configure(api_key=api_key)

# Create model instance (using latest recommended model)
model = genai.GenerativeModel('gemini-2.0-flash')

def AIresponse(prompt):
    try:
        response = model.generate_content(prompt)
        
        # Proper way to extract text from Gemini response
        if response.candidates:
            if hasattr(response.candidates[0].content, 'parts'):
                return response.candidates[0].content.parts[0].text
        return response.text
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

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
    intro = AIresponse(prompt)
    return intro or "The vault doors loom before you..."  # Fallback if API fails

def clean_json_response(text):
    """Remove markdown formatting and extract pure JSON"""
    text = text.replace('```json', '').replace('```', '').strip()
    return text

def get_challenge(attempt, intro_context):
    prompt = (
        f"Based on this heist introduction:\n{intro_context}\n\n"
        f"Create security challenge #{attempt} with:\n"
        "1. Description referencing a specific Pentagon security measure\n"
        "2. 3 tool options (one correct, two decoys)\n"
        "3. Explicit correct option\n"
        "4. Failure consequence\n"
        "5. Code value (format: WORD-WORD-###)\n"
        "6. Subtle hint related to introduction\n\n"
        "Output STRICT JSON ONLY (no markdown) like:\n"
        "{\"description\": \"...\", \"options\": [...], \"correct\": \"...\", \"failure\": \"...\", \"Code\": \"...\", \"hint\": \"...\"}"
    )
    
    try:
        response = AIresponse(prompt)
        if not response:
            raise ValueError("Empty API response")
            
        # Clean the response
        cleaned = clean_json_response(response)
        
        # Parse and validate
        challenge = json.loads(cleaned)
        
        # Validation checks
        required_keys = ["description", "options", "correct", "failure", "Code", "hint"]
        for key in required_keys:
            if key not in challenge:
                raise ValueError(f"Missing key: {key}")
                
        if len(challenge["options"]) != 3:
            raise ValueError("Need exactly 3 options")
            
        # Normalize options and correct answer
        options = [str(opt).strip() for opt in challenge["options"]]
        correct = str(challenge["correct"]).strip()
        
        # Ensure correct answer is in options
        if correct not in options:
            options[0] = correct  # Replace first option if missing
            
        # Shuffle while maintaining correct index
        correct_index = options.index(correct)
        random.shuffle(options)
        new_correct = options.index(correct)
        
        # Update challenge object
        challenge["options"] = options
        challenge["correct"] = correct
        
        return challenge
        
    except Exception as e:
        print(f"Challenge Error: {str(e)}")
        # Fallback challenge
        return {
            "description": "A holographic guard materializes, scanning for intruders...",
            "options": ["Cloaking device", "Sensor hack", "Noise distraction"],
            "correct": "Sensor hack",
            "failure": "Hologram alerts security!",
            "Code": "HALO-OVERRIDE-404",
            "hint": "Remember the quantum decoherence weakness mentioned earlier..."
        }


