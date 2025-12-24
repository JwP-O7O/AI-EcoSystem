#!/bin/bash
# AI EcoSystem Backend Gateway Starter

cd "$(dirname "$0")"

echo "🔧 Checking dependencies..."
pip install -q -r requirements.txt

echo "🚀 Starting AI EcoSystem Gateway..."
python gateway.py
