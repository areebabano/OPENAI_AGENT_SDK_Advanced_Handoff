# Handoffs in OpenAI Agent SDK

Handoffs allow an agent to delegate tasks to another agent. This is particularly useful in scenarios where different agents specialize in distinct areas. For example, a customer support app might have agents that specifically handle tasks like order status, refunds, FAQs, etc.

Handoffs are represented as **tools** to the LLM. For example, a handoff to an agent named `Refund Agent` will have the tool name `transfer_to_refund_agent`.

---

## Creating a Handoff

All agents have a `handoffs` parameter, which can either take an `Agent` directly or a `Handoff` object for customization.

You can create a handoff using the `handoff()` function provided by the Agents SDK. This allows specifying the agent to hand off to, along with optional overrides and input filters.

### Basic Usage

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

triage_agent = Agent(
    name="Triage agent",
    handoffs=[billing_agent, handoff(refund_agent)]
)
```

## Customizing Handoffs via `handoff()`

The `handoff()` function allows customization:

| Parameter                | Description                                                                                   |
|--------------------------|-----------------------------------------------------------------------------------------------|
| `agent`                  | The agent to which the conversation will be handed off.                                        |
| `tool_name_override`     | Override the default tool name (`transfer_to_<agent_name>`).                                   |
| `tool_description_override` | Override the default tool description.                                                      |
| `on_handoff`             | Callback executed when handoff is invoked. Receives the agent context and optionally LLM input. |
| `input_type`             | Type of input expected by the handoff (optional).                                             |
| `input_filter`           | Function to filter input passed to the next agent.                                           |
| `is_enabled`             | Boolean or function to dynamically enable/disable the handoff.                               |

### Example:
---
```python
from agents import Agent, handoff, RunContextWrapper

def on_handoff(ctx: RunContextWrapper[None]):
    print("Handoff called")

agent = Agent(name="My agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="Custom description",
)
```

## Handoff Inputs

Sometimes the LLM needs to provide data when a handoff occurs. For example, when handing off to an "Escalation agent", you may want a reason for the escalation.

```python
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

agent = Agent(name="Escalation agent")

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
)

```

## Input Filters

By default, when a handoff occurs, the new agent sees the entire previous conversation. To modify this, you can set an input_filter. It receives the existing input and must return a new HandoffInputData.

Common patterns (e.g., removing all tool calls from history) are implemented in agents.extensions.handoff_filters.

```python
from agents import Agent, handoff
from agents.extensions import handoff_filters

agent = Agent(name="FAQ agent")

handoff_obj = handoff(
    agent=agent,
    input_filter=handoff_filters.remove_all_tools,
)

```

## Recommended Prompts

To ensure LLMs understand handoffs properly, include information about handoffs in your agent instructions. Use the recommended prompt from agents.extensions.handoff_prompt.

```python
from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

billing_agent = Agent(
    name="Billing agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    <Fill in the rest of your prompt here>.""",
)

```

### Alternatively, use:

from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


This automatically adds recommended data to your prompts.

## Summary

- Handoffs enable delegation to specialized agents.

- Use handoff() for creating customized handoffs.

- Optionally handle inputs and filters to control the conversation flow.

- Include recommended instructions in prompts to ensure the LLM correctly handles handoffs.