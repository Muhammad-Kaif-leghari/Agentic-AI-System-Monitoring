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

def get_ram_utilization() -> str:
    """
    Checks and returns the current RAM (Memory) usage percentage of the local computer.
    Use this tool whenever the user asks about memory, RAM, background apps consuming space,
    or if they ask if they have enough free memory left to run programs.
    """
    ram_info = psutil.virtual_memory()
    return f"Current Ram Usage is: {ram_info.percent}% (Used {ram_info.used / (1024**3):.2f} GB / Total: {ram_info.total / (1024**3): .2f} GB)" 

# We pass our Python function inside a list to the config object
agent_tools = [get_cpu_utilization, get_ram_utilization]
print("\n")
print("System Monitoring Agent is Online! Type 'exit', 'quit', 'q' or 'close' to stop.")
print("-" * 50)
 
while True:
    user_prompt = input("\nYou:")

    if user_prompt.lower() in ["exit", "quit", "q", "close"]:
        print("Shutting down agent. Goodbye!")
        break
        
    if not user_prompt.strip():
        continue

    
    print("Agent is processing...")

    try:
        # 3. Send a simple message to the flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                tools=agent_tools,
            )
        )

        print(f"\nGemini Response: {response.text}")

    except Exception as e:
        print(f"An Error occurred: {e}")