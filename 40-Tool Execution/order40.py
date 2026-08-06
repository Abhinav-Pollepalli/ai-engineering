from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("api key not found")


client = genai.Client(api_key=API_KEY)

weather_tool_declaration = {
    "type":"function",
    "name":"weather_tool",
    "description":"Use this tool to find the weather given a location",
    "parameters":{
        "type":"object",
        "properties":{
            "city":{"type":"string", "description":"This is the name of the city that you are trying to find the weather of ex. San Francisco"},
        },
    },
    "required":["city"],
}

def weather_tool(city:str):
    return {"city":city, "weather": "85.2 degrees fahrenheit"}


set_temp_tool_declaration = {
    "type":"function",
    "name":"set_temp_tool",
    "description":"This tool lets you set the temp for lights",
    "parameters":{
        "type":"object",
        "properties":{
            "temperature":{"type":"integer", "description":"temperature range is in kelvin 2000 means warm/ orange light, 10000 means blue/white color "},
            "location":{"type":"string", "description":"need location to locate the light ex. office room, bedroom, bathroom"}
        },
        "required":["temperature", "location"]
    }

}

def set_temp_tool(temperature, location):
    return {"message":f"{location}'s light has been set to {temperature}k"}


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input= "gimme temperatue",
    tools=[weather_tool_declaration, set_temp_tool_declaration]
)



step_type = None
step_name = None
step_id = None

for step in interaction.steps:
    
    if step.type == "model_output":
        print(interaction.output_text)
        step_type = step.type

    elif step.type == "function_call":
        step_type = step.type
        if "weather_tool" in step.name:
            step_name = step.name
            step_id = step.id
            result = weather_tool(**step.arguments)
            break

        if "set_temp_tool" in step.name:
            step_name = step.name
            step_id = step.id
            result = set_temp_tool(**step.arguments)
            break



if step_type == "function_call":
    final_interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=[
            {
                "type":"function_result",
                "name":step_name,
                "call_id":step_id,
                "result":[{"type":"text", "text":json.dumps(result)}]
            }
        ],  
        tools=[weather_tool_declaration, set_temp_tool_declaration],
        previous_interaction_id=interaction.id
    )


    print(f"LLM FINAL ANSWER: {final_interaction.output_text}")