import streamlit as st
from openai import OpenAI
import os
import tempfile
import json
from typing import List, Dict, Any
import pandas as pd
from io import StringIO
import base64
import PyPDF2
from docx import Document

# Configure page
st.set_page_config(
    page_title="AI File Insights Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📊 AI File Insights Extractor")
    st.markdown("Upload your files and get AI-powered insights using OpenAI's API")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # OpenAI API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. You can get one from https://platform.openai.com/api-keys"
        )
        
        # Model selection
        model = st.selectbox(
            "Select Model",
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0,
            help="Choose the OpenAI model for analysis"
        )
        
        # Analysis type
        analysis_type = st.selectbox(
            "Analysis Type",
            ["General Insights", "Data Analysis", "Document Summary", "Custom Analysis"],
            help="Select the type of analysis you want to perform"
        )
        
        if analysis_type == "Custom Analysis":
            custom_prompt = st.text_area(
                "Custom Analysis Prompt",
                placeholder="Describe what specific insights you want to extract...",
                height=100
            )
        else:
            custom_prompt = None
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 File Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files to analyze",
            accept_multiple_files=True,
            type=['txt', 'csv', 'json', 'pdf', 'docx', 'xlsx', 'md'],
            help="Upload one or more files for AI analysis"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
            
            # Display file information
            for file in uploaded_files:
                st.write(f"📄 **{file.name}** ({file.size} bytes)")
    
    with col2:
        st.header("🤖 Analysis Results")
        
        if uploaded_files and api_key:
            if st.button("🚀 Analyze Files", type="primary"):
                analyze_files(uploaded_files, api_key, model, analysis_type, custom_prompt)
        elif not api_key:
            st.warning("⚠️ Please enter your OpenAI API key in the sidebar")
        elif not uploaded_files:
            st.info("ℹ️ Please upload files to analyze")

def get_file_content(uploaded_file) -> str:
    """Extract content from uploaded file based on file type."""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension in ['txt', 'md']:
            return str(uploaded_file.read(), "utf-8")
        elif file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            return f"CSV Data Summary:\n{df.describe()}\n\nFirst 10 rows:\n{df.head(10).to_string()}"
        elif file_extension == 'json':
            data = json.load(uploaded_file)
            return f"JSON Data:\n{json.dumps(data, indent=2)[:2000]}..."  # Limit size
        elif file_extension == 'xlsx':
            df = pd.read_excel(uploaded_file)
            return f"Excel Data Summary:\n{df.describe()}\n\nFirst 10 rows:\n{df.head(10).to_string()}"
        elif file_extension == 'pdf':
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages[:10]:  # Limit to first 10 pages
                text += page.extract_text() + "\n"
            return text[:5000]  # Limit text length
        elif file_extension == 'docx':
            # Extract text from DOCX
            doc = Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text[:5000]  # Limit text length
        else:
            # For other file types, try to read as text
            return str(uploaded_file.read(), "utf-8", errors='ignore')[:2000]
    except Exception as e:
        return f"Error reading file {uploaded_file.name}: {str(e)}"

def get_analysis_prompt(analysis_type: str, custom_prompt: str = None) -> str:
    """Generate appropriate prompt based on analysis type."""
    if analysis_type == "Custom Analysis" and custom_prompt:
        return custom_prompt
    
    prompts = {
        "General Insights": """
        Analyze the provided file content and extract key insights. Focus on:
        1. Main themes and patterns
        2. Important data points or findings
        3. Potential areas of interest or concern
        4. Summary of key takeaways
        5. Actionable recommendations if applicable
        """,
        "Data Analysis": """
        Perform a comprehensive data analysis on the provided content. Include:
        1. Data structure and quality assessment
        2. Statistical summaries and trends
        3. Anomalies or outliers
        4. Correlations and relationships
        5. Business insights and recommendations
        """,
        "Document Summary": """
        Create a comprehensive summary of the document including:
        1. Executive summary
        2. Key points and main arguments
        3. Important facts and figures
        4. Conclusions and recommendations
        5. Action items if any
        """
    }
    
    return prompts.get(analysis_type, prompts["General Insights"])

def analyze_files(uploaded_files: List, api_key: str, model: str, analysis_type: str, custom_prompt: str = None):
    """Analyze uploaded files using OpenAI API."""
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, file in enumerate(uploaded_files):
        try:
            status_text.text(f"Processing {file.name}...")
            progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Get file content
            file_content = get_file_content(file)
            
            # Check if file content extraction was successful
            if file_content.startswith("Error reading file"):
                results.append({
                    "file_name": file.name,
                    "insights": file_content,
                    "tokens_used": 0
                })
                continue
            
            # Prepare prompt
            analysis_prompt = get_analysis_prompt(analysis_type, custom_prompt)
            
            # Create messages for OpenAI API
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert data analyst and insights extractor. Provide detailed, actionable insights based on the provided content."
                },
                {
                    "role": "user",
                    "content": f"""
                    File: {file.name}
                    
                    Analysis Request: {analysis_prompt}
                    
                    File Content:
                    {file_content}
                    
                    Please provide a detailed analysis with clear insights and recommendations.
                    """
                }
            ]
            
            # Make API call to OpenAI
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2000,
                temperature=0.1
            )
            
            # Extract insights
            insights = response.choices[0].message.content
            
            results.append({
                "file_name": file.name,
                "insights": insights,
                "tokens_used": response.usage.total_tokens
            })
            
        except Exception as e:
            st.error(f"Error analyzing {file.name}: {str(e)}")
            results.append({
                "file_name": file.name,
                "insights": f"Error: {str(e)}",
                "tokens_used": 0
            })
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Display results
    display_results(results)

def display_results(results: List[Dict[str, Any]]):
    """Display analysis results in a user-friendly format."""
    
    st.header("📊 Analysis Results")
    
    # Summary metrics
    total_files = len(results)
    total_tokens = sum(result.get('tokens_used', 0) for result in results)
    successful_analyses = sum(1 for result in results if not result['insights'].startswith('Error:'))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Files Analyzed", total_files)
    with col2:
        st.metric("Successful Analyses", successful_analyses)
    with col3:
        st.metric("Total Tokens Used", total_tokens)
    
    # Individual file results
    for i, result in enumerate(results):
        with st.expander(f"📄 {result['file_name']} - Analysis Results", expanded=i == 0):
            if result['insights'].startswith('Error:'):
                st.error(result['insights'])
            else:
                st.markdown(result['insights'])
                
                # Add download button for insights
                st.download_button(
                    label=f"📥 Download Insights for {result['file_name']}",
                    data=result['insights'],
                    file_name=f"{result['file_name']}_insights.txt",
                    mime="text/plain"
                )
    
    # Download all results
    if results:
        all_insights = "\n\n" + "="*50 + "\n\n".join([
            f"File: {result['file_name']}\n\nInsights:\n{result['insights']}"
            for result in results
        ])
        
        st.download_button(
            label="📥 Download All Insights",
            data=all_insights,
            file_name="all_insights.txt",
            mime="text/plain",
            type="secondary"
        )

if __name__ == "__main__":
    main()