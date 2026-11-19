#!/usr/bin/env bash
# Create (or reuse) the single-node kind cluster used in Modules 3, 5 and 9.
set -euo pipefail
if kind get clusters 2>/dev/null | grep -qx genai-labs; then
  echo "Cluster genai-labs already exists"; else kind create cluster --name genai-labs --wait 120s; fi
kubectl cluster-info --context kind-genai-labs
kubectl get nodes
