#!/bin/bash
# Script to start the Streamlit application

echo "🚀 Starting Nachrichten Kategorisierer..."
echo "📧 Message Categorization Application"
echo "=" * 50

# Activate virtual environment
source venv/bin/activate

# Start Streamlit application
echo "🌐 Starting Streamlit server..."
echo "📍 Application will be available at: http://localhost:8501"
echo ""
echo "💡 Don't forget to:"
echo "   1. Add your OpenAI API key in the sidebar"
echo "   2. Upload .msg files for categorization"
echo ""

streamlit run app.py