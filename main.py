# ----------------------------- ADVANCED_HANDOFF --------------------------------------

import asyncio

from config import model

from custom_handoff.customization_handoff import math_teacher

from agents import (
    Agent,
    function_tool,
    Runner,
)

@function_tool
async def weather(city:str) -> str:
    """Weather Tool"""
    print("------------------Weather Tool Call-----------------------------")
    return f"{city} weather is sunny."


assistant: Agent = Agent(
    name="Helpful Assistant",
    instructions="""
    You are a helpful assistant.  
    - If the user’s query is **related to math**, use the `math_teacher` handoff.  
    - If the user’s query is **related to weather**, use the `weather` tool.  
    - For any other query, respond directly without calling a tool or handoff.  
    """,
    model=model,
    handoffs=[math_teacher],
    tools=[weather]
)

print(assistant.handoffs)

def main():
    result: Runner = Runner.run_sync(
        assistant,
        "What is the weather in karachi? and 2+10=?",
        context={"name": "Areeba Hammad", "age": 20, "role": "student"}
    )

    print(result.last_agent)
    print(result.final_output)

if __name__ == "__main__":
    main()