#!/bin/bash

# German Stock Market Tracker - Startup Script

echo "🚀 Starting German Stock Market Tracker..."
echo "📈 This application tracks German stocks with AI-powered analysis"
echo "🔍 Now with web search integration for latest market news and updates!"
echo ""

# Check if streamlit is available
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Add local bin to PATH if needed
export PATH="/home/ubuntu/.local/bin:$PATH"

echo "🌐 Starting Streamlit application..."
echo "📍 The app will be available at: http://localhost:8501"
echo "🔑 Remember to add your OpenAI API key in the sidebar to enable chat features!"
echo ""

# Start the application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0