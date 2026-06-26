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
    Checks and returns both the current RAM utilization and the total installed RAM capacity.
    Use this tool whenever the user asks about memory, RAM, total RAM, hardware capacity, 
    specifications, background apps consuming space, or free memory.
    """
    ram_info = psutil.virtual_memory()
    percent = ram_info.percent
    used_ram_info = ram_info.used / (1024**3)
    total_ram_info = ram_info.total / (1024**3)
    return f"Current Ram Usage is: {percent}% | (Used RAM: {used_ram_info:.2f} GB / Total Installed RAM: {total_ram_info:.2f} GB)" 

def get_storage_metrics() -> str:
    """
    Checks and returns the local hard drive storage metrics (Disk capacity and availability).
    Use this tool whenever the user asks about disk space, hard drive, storage, C: drive,
    remaining space, or full disk capacity.
    """
    disk_info = psutil.disk_usage("C:\\")
    used_space_gb =  disk_info.used / (1024**3)
    total_space_gb = disk_info.total / (1024**3)
    free_space_gb =  disk_info.free / (1024**3)
    percent = disk_info.percent
    return f"C:\\ Drive Status: Total Capacity {total_space_gb:.2f} GB | Used Space: {used_space_gb:.2f} GB | Free space available: {free_space_gb:.2f} GB | Percent usage total: {percent}% "

# Pass Python function inside a list to the config object
agent_tools = [get_cpu_utilization, get_ram_utilization, get_storage_metrics]
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