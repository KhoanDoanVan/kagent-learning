# Basic LangGraph Agent

This is a basic LangGraph agent that can be used to test KAgent BYO (Bring Your Own) agent with ADK (Agent Development Kit). This agent provides currency conversion functionality using Google's Gemini model.

## Prerequisites

- Docker Desktop installed and running
- kubectl installed  
- kind installed
- Kind cluster running (e.g., `kind create cluster --name kagent-cluster`)
- kagent installed and running in the cluster

## Setup Instructions

### 1. Set Environment Variables

```bash
# Set required API keys
export OPENAI_API_KEY=your_openai_api_key_here
export GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Project Structure

Ensure your project has the following structure:

```
basic_langgraph_agent/
├── agent/
│   ├── __init__.py
│   ├── agent-card.json
│   ├── cli.py
│   ├── graph.py
│   ├── instructions.py
│   └── tools.py
├── Dockerfile
├── agent.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

### 3. Build and Load the Agent Image

```bash
# Build the image locally
docker build -t basic-currency-agent:v7 .

# Load the image directly into your Kind cluster
kind load docker-image basic-currency-agent:v7 --name kagent-cluster
```

### 4. Create Secret with Google API Key

```bash
kubectl create secret generic kagent-langgraph-google -n kagent --from-literal=GOOGLE_API_KEY=$GOOGLE_API_KEY
```

### 5. Deploy the Agent

```bash
kubectl apply -f agent.yaml
```

### 6. Verify Deployment

```bash
# Check agent status
kubectl get agents -n kagent

# Check pods are running
kubectl get pods -n kagent

# View agent details
kubectl describe agent basic-currency-langgraph-a2a-agent -n kagent

# Check agent logs
kubectl logs -l app=basic-currency-langgraph-a2a-agent -n kagent
```

### 7. Access the Agent

```bash
# Start port forwarding (in a separate terminal)
kubectl port-forward svc/kagent-controller 8083:8083 -n kagent

# Test with get the card of the agent (in a separate terminal)
curl localhost:8083/api/a2a/kagent/basic-agent/.well-known/agent.json
```

## Agent Features

This LangGraph agent provides:

- **Currency Conversion**: Real-time exchange rates using the Frankfurter API
- **Google Gemini Integration**: Uses Google's Gemini 2.0 Flash model
- **KAgent Framework**: Full integration with kagent checkpointing and tools
- **REAct Pattern**: Uses LangGraph's prebuilt ReAct agent for tool usage

## Dependencies

The agent includes these key dependencies:

- `kagent-langgraph`: KAgent LangGraph integration
- `langgraph`: Graph-based agent framework
- `langchain-google-genai`: Google Gemini model integration
- `starlette` & `sse-starlette`: HTTP server dependencies
- `anthropic` & `openai`: OpenTelemetry instrumentation dependencies
- `httpx`: HTTP client for API calls

## Troubleshooting

### If ImagePullBackOff occurs:
- Ensure you've loaded the image into Kind: `kind load docker-image basic-currency-agent:v7 --name kagent-cluster`
- Verify the image tag in `agent.yaml` matches the loaded image

### If agent is not ready:
- Check pod logs: `kubectl logs -l app=basic-currency-langgraph-a2a-agent -n kagent`
- Ensure secrets exist in the correct namespace: `kubectl get secrets -n kagent`
- Verify all dependencies are installed in `uv.lock`

### If import errors occur:
- Ensure `agent/__init__.py` exists and imports the graph
- Check that `sys.path.insert(0, '/app')` is in `cli.py`
- Verify no naming conflicts between files and packages

### If missing dependency errors:
- Regenerate lock file: `rm uv.lock && uv lock`
- Rebuild image with updated dependencies
- Check that all required packages are in `pyproject.toml`

### If port-forward fails:
- Check what's using port 8083: `lsof -i :8083`
- Use a different port: `kubectl port-forward svc/