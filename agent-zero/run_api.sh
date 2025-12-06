#!/bin/bash
echo "🚀 Starting Synapse OS API Backend..."
cd $(dirname "$0")
export PYTHONPATH=$PYTHONPATH:$(pwd)
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
