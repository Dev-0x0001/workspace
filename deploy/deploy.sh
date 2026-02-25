# Deployment Script

#!/bin/bash
# Script to deploy code to production

# Configuration
REPO_OWNER='Dev-0x0001'
REPO_NAME='workspace'
BRANCH='main'

# Deploy Docker containers
echo "Building Docker image..."
docker build -t dev-0x0001/workspace:latest .

echo "Pushing Docker image..."
docker push dev-0x0001/workspace:latest

# Update Kubernetes deployment
kubectl set image deployment/workspace deployment=dev-0x0001/workspace:latest

# Verify deployment
echo "Checking deployment status..."
kubectl rollout status deployment/workspace