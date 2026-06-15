import os
from dotenv import load_dotenv
from google import genai

# 1. Load environment variables from the hidden .env file
load_dotenv()
# 2. Initialize the Gemini client (it automatically looks for GEMINI_API_KEY in your env)
client = genai.Client()

print("Testing connection to Gemini brain...")

# 3. Send a simple message to the flash model
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Tell me in three words what an AI agent is.',
)

print("\nGemini Response:")
print(response.text)