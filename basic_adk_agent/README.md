# Basic Agent

This is a basic agent that can used to test KAgent BYO agent with ADK.

1. Build the agent image

```bash
# Start a local registry
docker run -d -p 5001:5000 --name registry registry:2
```

```bash
# Push to registry (only if you have a registry running)
docker build  . --push -t localhost:5001/my-byo:latest
```

1. Create a secret with the google api key

```bash
kubectl create secret generic kagent-google -n kagent  --from-literal=GOOGLE_API_KEY=$GOOGLE_API_KEY   --dry-run=client -oyaml | k apply -f -
```

3. Deploy the agent

```bash
kubectl apply -f agent.yaml
```