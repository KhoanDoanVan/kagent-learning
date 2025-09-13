

from google.adk import Agent
from .tools import roll_die, check_prime
from .instruction import INSTRUCTION


root_agent = Agent(
    model="gemini-2.0-flash",
    name="hello_world_agent",
    description=("hello world agent that can roll a dice of 8 sides and check prime numbers."),
    instruction=INSTRUCTION,
    tools=[roll_die, check_prime],
)