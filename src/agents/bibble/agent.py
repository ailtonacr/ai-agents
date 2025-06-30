from google.adk.agents import Agent
from .prompts import BIBBLE_PROMPT, BIBBLE_DESCRIPTION, BIBBLE_MODEL

root_agent = Agent(
    model=BIBBLE_MODEL,
    name="Bibble",
    description=BIBBLE_DESCRIPTION,
    instruction=BIBBLE_PROMPT,
)
