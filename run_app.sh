#!/bin/bash

# 3D Avatar Generator Startup Script
echo "🎭 Starting 3D Avatar Generator..."
echo "📋 Make sure you have your OpenAI API key ready!"
echo ""

# Activate virtual environment and run Streamlit
source venv/bin/activate
streamlit run avatar_generator.py --server.headless true --server.port 8501 --server.address 0.0.0.0