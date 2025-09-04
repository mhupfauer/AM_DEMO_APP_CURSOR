import streamlit as st
import openai
from PIL import Image
import io
import base64
import requests
from datetime import datetime

def main():
    st.set_page_config(
        page_title="3D Avatar Generator",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🎭 3D Avatar Generator")
    st.markdown("Transform photos into funny 3D cartoon avatars using AI!")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to use DALL-E 3 for avatar generation"
        )
        
        if api_key:
            st.success("✅ API Key provided")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        st.markdown("### ℹ️ How it works")
        st.markdown("""
        1. Upload a photo of the person
        2. The AI will analyze the photo
        3. Generate a 3D cartoon avatar
        4. Download your creation!
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Photo")
        uploaded_file = st.file_uploader(
            "Choose a photo to transform",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of the person you want to turn into a 3D avatar"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Photo", use_column_width=True)
            
            # Convert image to base64 for API
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    with col2:
        st.header("🎨 Generated Avatar")
        
        if uploaded_file is not None and api_key:
            if st.button("🚀 Generate 3D Avatar", type="primary"):
                with st.spinner("Creating your 3D avatar... This may take a moment!"):
                    try:
                        # Generate avatar using OpenAI DALL-E 3
                        avatar_url = generate_avatar(api_key, img_base64)
                        
                        if avatar_url:
                            # Display generated avatar
                            st.image(avatar_url, caption="Your 3D Avatar", use_column_width=True)
                            
                            # Download button
                            avatar_image = download_image(avatar_url)
                            if avatar_image:
                                st.download_button(
                                    label="💾 Download Avatar",
                                    data=avatar_image,
                                    file_name=f"3d_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                    mime="image/png"
                                )
                        else:
                            st.error("❌ Failed to generate avatar. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Error generating avatar: {str(e)}")
        
        elif not api_key:
            st.info("👈 Please enter your OpenAI API key in the sidebar")
        elif not uploaded_file:
            st.info("👈 Please upload a photo to get started")


def generate_avatar(api_key, img_base64):
    """Generate 3D avatar using OpenAI DALL-E 3 with GPT-4 Vision analysis"""
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # First, analyze the uploaded image using GPT-4 Vision
        st.info("🔍 Analyzing the uploaded photo...")
        analysis_response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this photo and describe the person's key physical features, hair color/style, clothing, and any distinctive characteristics. Be specific but concise. Focus on features that would be recognizable in a cartoon avatar."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        # Get the analysis
        analysis = analysis_response.choices[0].message.content
        st.success("✅ Photo analyzed successfully!")
        
        # Create a personalized prompt based on the analysis
        personalized_prompt = f"""Create a 3D cartoon-style character based on this description: {analysis}

Transform this person into a polished, smooth, glossy cartoon style with large expressive eyes and a friendly expression. Preserve their recognizable facial features, hair color, hairstyle, and overall look from the description. Recreate their outfit, adapting it into the same stylized cartoon aesthetic, including any key accessories or details mentioned. Pose them in a confident, neutral standing position from head to feet with a transparent background. Please show the full body. Make it cute, modern, and suitable for use as a fun avatar."""

        # Generate image using DALL-E 3
        st.info("🎨 Generating your 3D avatar...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=personalized_prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        
        return response.data[0].url
        
    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return None


def download_image(url):
    """Download image from URL and return as bytes"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        st.error(f"Error downloading image: {str(e)}")
        return None


if __name__ == "__main__":
    main()