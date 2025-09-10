from pydantic import BaseModel

from config import model

from agents import Agent, function_tool, RunContextWrapper, handoff

from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from agents.extensions import handoff_filters

from policy.policy import policy_is_enabled


@function_tool
async def add(a:int, b:int)-> int:
    """Addition Tool"""
    print("------------------Add Tool Call-----------------------------")
    return a + b 

math_assistant: Agent = Agent(
    name="Math Teacher",
    instructions=f""" {RECOMMENDED_PROMPT_PREFIX}
    You are a helpful math teacher agent.
    """,
    model=model,
    tools=[add],
    handoff_description="This is a special Math Assistant."
)

class InputData(BaseModel):
    reason: str

async def on_handoff_data(ctx: RunContextWrapper, input_data: InputData):
    print("context: ",ctx.context)
    print("Reason: ", input_data.reason) # print reason

math_teacher = handoff(
    agent=math_assistant,
    tool_name_override="special_math_teacher",
    tool_description_override="This is a special Mathematics Teacher.",
    on_handoff= on_handoff_data,
    input_type=InputData,
    input_filter=handoff_filters.remove_all_tools,
    is_enabled=policy_is_enabled
)
