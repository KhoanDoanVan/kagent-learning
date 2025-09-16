
import logging
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import faulthandler
import os
from google.adk.agents import BaseAgent
from a2a.types import AgentCard
from .utils._token import KAgentTokenService
import httpx
from google.adk.runners import Runner


logger = logging.getLogger(__name__)




def health_check(request: Request) -> PlainTextResponse:
  return PlainTextResponse("OK")


def thread_dump(request: Request) -> PlainTextResponse:
  import io
  
  buf = io.StringIO()
  faulthandler.dump_traceback(file=buf)
  
  buf.seek(0)
  return PlainTextResponse(buf.read())



kagent_url_override =  os.getenv("KAGENT_URL")


class SimonKAgentApp:
  
  def __init__(
    self,
    root_agent: BaseAgent,
    agent_card: AgentCard,
    kagent_url: str,
    app_name: str
  ):
    self.root_agent = root_agent
    self.kagent_url = kagent_url
    self.app_name = app_name
    self.agent_card = agent_card
    
  
  def build(self) -> FastAPI:
    
    token_service = KAgentTokenService(self.app_name)
    http_client = httpx.AsyncClient(
      base_url=kagent_url_override or self.kagent_url,
      event_hooks=token_service.event_hooks()
    )
    
    
    def create_runner() -> Runner:
      return Runner(
        agent=self.root_agent,
        app_name=self.app_name,
        session_service=se
      )
  
  