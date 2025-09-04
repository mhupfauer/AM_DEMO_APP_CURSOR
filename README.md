# 🎭 3D Avatar Generator

A Streamlit web application that transforms photos into funny 3D cartoon avatars using OpenAI's DALL-E 3.

## Features

- 📸 Upload photos of people
- 🔍 AI-powered photo analysis using GPT-4 Vision
- 🎨 Generate personalized 3D cartoon-style avatars
- 💾 Download generated avatars
- 🔑 Secure API key input via sidebar
- 🎯 Uses latest DALL-E 3 and GPT-4 Vision technology for high-quality, personalized results

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run avatar_generator.py
```

3. Open your browser to the provided URL (usually http://localhost:8501)

## Usage

1. **Enter API Key**: In the sidebar, enter your OpenAI API key
2. **Upload Photo**: Upload a clear photo of the person you want to transform
3. **Generate Avatar**: Click the "Generate 3D Avatar" button
   - The app will first analyze the photo using GPT-4 Vision
   - Then generate a personalized 3D avatar using DALL-E 3
4. **Download**: Once generated, download your 3D avatar using the download button

## Requirements

- OpenAI API key with access to DALL-E 3 and GPT-4 Vision
- Python 3.8+
- Internet connection

## API Key

You'll need an OpenAI API key to use this application. Get one from:
https://platform.openai.com/api-keys

The API key is entered securely through the sidebar and is not stored anywhere.

## Avatar Generation Process

The app uses a two-step AI process:

1. **Photo Analysis (GPT-4 Vision)**:
   - Analyzes facial features, hair color/style, clothing
   - Identifies distinctive characteristics
   - Creates detailed description for avatar generation

2. **Avatar Creation (DALL-E 3)**:
   - Generates personalized 3D cartoon-style characters
   - Preserves recognizable facial features and hairstyles
   - Creates glossy, polished cartoon aesthetic
   - Adds large expressive eyes and friendly expressions
   - Shows full body poses with transparent backgrounds
   - Recreates outfits in cartoon style

This ensures each avatar is uniquely tailored to the uploaded photo!

Enjoy creating your funny 3D avatars! 🎉