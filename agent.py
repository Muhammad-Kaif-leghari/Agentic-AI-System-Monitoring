import os
import psutil
from dotenv import load_dotenv
from google import genai
from google.genai import types


# 1. Load environment variables from the hidden .env file and temporarily loads it directly in your terminal's memory.
load_dotenv()
# 2. Initialize the Gemini client to build live connection object (it automatically looks for GEMINI_API_KEY in your env).
client = genai.Client()

def get_cpu_utilization() -> str:
    """
    Checks and returns the current CPU usage percentage of the local computer.
    Use this tool whenever the user asks about system health, CPU load, performance, 
    or if the machine is running slow.
    """
    cpu_percentage = psutil.cpu_percent(interval=1)
    return f"Current Cpu Usage is: {cpu_percentage}%"

# We pass our Python function inside a list to the config object
agent_tools = [get_cpu_utilization]

print("Agent is online and monitoring system health...")
print("-" * 50)

user_prompt = "Hey! My computer feels like it is lagging a bit. Can you check my system health and tell me if my CPU is working too hard?"
print(f"User: {user_prompt}\n")

# 3. Send a simple message to the flash model
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=user_prompt,
    config=types.GenerateContentConfig(
    tools=agent_tools,
)
)

print("\nGemini Response:")
print(response.text)