#!/usr/bin/env python3
"""
Simple script to run the Streamlit application.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit is not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if other dependencies are available
    try:
        import openai
        import pandas
        import PyPDF2
        import docx
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("🚀 Starting AI File Insights Extractor...")
    print("📊 The application will open in your default browser")
    print("🔑 Don't forget to enter your OpenAI API key in the sidebar!")
    print("\n" + "="*50)
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()