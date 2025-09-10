from agents import Agent, RunContextWrapper

async def policy_is_enabled(ctx: RunContextWrapper, agent: Agent):
    if ctx.context["age"] >= 18:
        return True
    return False