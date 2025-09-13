
from kagent.core import KAgentConfig
from kagent.langgraph import KAgentCheckpointer
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from agent.tools import get_exchange_rate
from agent.instructions import SYSTEM_INSTRUCTION
import httpx
import logging

logger = logging.getLogger(__name__)

kagent_checkpointer = KAgentCheckpointer(
    client=httpx.AsyncClient(base_url=KAgentConfig().url),
    app_name=KAgentConfig().app_name,
)


graph = create_react_agent(
  model=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
  tools=[get_exchange_rate],
  checkpointer=kagent_checkpointer,
  prompt=SYSTEM_INSTRUCTION,
)