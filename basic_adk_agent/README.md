# Basic Agent

This is a basic agent that can be used to test KAgent BYO agent with ADK.

## Prerequisites

- Docker Desktop installed and running
- kubectl installed  
- kind installed
- Kind cluster running (e.g., `kind create cluster --name kagent-cluster`)

## Setup Instructions

### 1. Set Environment Variables

```bash
# Set required API keys
export OPENAI_API_KEY=your_openai_api_key_here
export GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Build and Load the Agent Image

```bash
# Build the image locally
docker build -t my-byo:latest .

# Load the image directly into your Kind cluster
kind load docker-image my-byo:latest --name kagent-cluster
```

### 3. Create Secret with Google API Key

```bash
kubectl create secret generic kagent-google -n kagent --from-literal=GOOGLE_API_KEY=$GOOGLE_API_KEY
```

### 4. Deploy the Agent

```bash
kubectl apply -f agent.yaml
```

### 5. Verify Deployment

```bash
# Check agent status
kubectl get agents -n kagent

# Check pods are running
kubectl get pods -n kagent

# View agent details
kubectl describe agent basic-agent -n kagent
```

### 6. Access the Agent

```bash
# Start port forwarding (in a separate terminal)
kubectl port-forward svc/kagent-controller 8083:8083 -n kagent

# Test with get the card of the agent (in a separate terminal)
curl localhost:8083/api/a2a/kagent/basic-agent/.well-known/agent.json
```

## Troubleshooting

### If ImagePullBackOff occurs:
- Ensure you've loaded the image into Kind: `kind load docker-image my-byo:latest --name kagent-cluster`
- Verify the image name in `agent.yaml` matches: `my-byo:latest` (no registry prefix)

### If agent is not ready:
- Check pod logs: `kubectl logs -l app=basic-agent -n kagent`
- Ensure secrets exist in the correct namespace: `kubectl get secrets -n kagent`

### If port-forward fails:
- Check what's using port 8083: `lsof -i :8083`
- Use a different port: `kubectl port-forward svc/kagent-controller 8084:8083 -n kagent`

## Cleanup

```bash
# Delete the agent
kubectl delete agent basic-agent -n kagent

# Delete the cluster (optional)
kind delete cluster --name kagent-cluster
```

## Notes

- This setup uses Kind's image loading feature instead of a registry, which is more reliable for local development
- The agent runs in the `kagent` namespace alongside other kagent components
- Make sure to replace API key placeholders with your actual keys