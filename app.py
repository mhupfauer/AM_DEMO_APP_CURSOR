import streamlit as st
import openai
from openai import OpenAI
import io
import PyPDF2
import docx
import pandas as pd
from typing import List, Dict, Any
import json
import tiktoken

# Page configuration
st.set_page_config(
    page_title="Document Quality Control",
    page_icon="📄",
    layout="wide"
)

# Constants
MAX_FILE_SIZE_MB = 10  # Maximum file size in MB
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_TOKENS = 8000  # Max tokens to send to GPT-4 (leaving room for response)
MAX_CHARS = 30000  # Approximate character limit for text

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return None

def extract_text_from_txt(txt_file):
    """Extract text from TXT file"""
    try:
        text = txt_file.read().decode('utf-8')
        return text
    except Exception as e:
        st.error(f"Error reading TXT: {str(e)}")
        return None

def estimate_tokens(text: str, model: str = "gpt-4") -> int:
    """Estimate the number of tokens in a text string"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback to rough estimate if tiktoken fails
        return len(text) // 4

def truncate_text_for_analysis(text: str, max_chars: int = MAX_CHARS) -> tuple[str, bool]:
    """Truncate text if it's too long, returns (truncated_text, was_truncated)"""
    if len(text) <= max_chars:
        return text, False
    
    # Try to truncate at a sentence boundary
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')
    
    # Use the latest sentence or paragraph boundary
    boundary = max(last_period, last_newline)
    if boundary > max_chars * 0.8:  # Only use boundary if it's not too far back
        truncated = truncated[:boundary + 1]
    
    return truncated, True

def analyze_document_quality(client: OpenAI, document_text: str, qa_criteria: List[str]) -> Dict[str, Any]:
    """Analyze document quality using OpenAI"""
    
    # Truncate document if it's too long
    truncated_text, was_truncated = truncate_text_for_analysis(document_text)
    
    criteria_text = "\n".join([f"- {criterion}" for criterion in qa_criteria])
    
    truncation_notice = ""
    if was_truncated:
        truncation_notice = "\n\nNOTE: This document was truncated for analysis due to size constraints. The analysis is based on the first portion of the document."
    
    prompt = f"""
    You are a document quality control specialist. Please analyze the following document against these quality assurance criteria:

    Quality Assurance Criteria:
    {criteria_text}

    Document Text:
    {truncated_text}{truncation_notice}

    Please provide a comprehensive quality analysis in JSON format with the following structure:
    {{
        "overall_score": <score from 1-10>,
        "overall_assessment": "<brief overall assessment>",
        "criteria_analysis": [
            {{
                "criterion": "<criterion text>",
                "score": <score from 1-10>,
                "assessment": "<detailed assessment>",
                "issues_found": ["<list of specific issues>"],
                "recommendations": ["<list of recommendations>"]
            }}
        ],
        "summary": {{
            "strengths": ["<list of document strengths>"],
            "weaknesses": ["<list of document weaknesses>"],
            "priority_improvements": ["<list of priority improvements>"]
        }}
    }}

    Be thorough and specific in your analysis. Provide actionable feedback.
    """

    try:
        # Check token count before sending
        estimated_tokens = estimate_tokens(prompt)
        if estimated_tokens > MAX_TOKENS:
            st.warning(f"Document is very large. Using a condensed version for analysis.")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert document quality analyst. Provide detailed, constructive feedback in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000  # Limit response size
        )
        
        # Parse the JSON response
        analysis = json.loads(response.choices[0].message.content)
        
        # Add truncation warning to analysis if applicable
        if was_truncated:
            analysis['truncation_warning'] = "This analysis is based on a truncated version of the document due to size constraints."
        
        return analysis
    except json.JSONDecodeError as e:
        st.error(f"Error parsing AI response: {str(e)}")
        return None
    except openai.BadRequestError as e:
        if "maximum context length" in str(e):
            st.error("Document is too large for analysis. Please upload a smaller document or split it into sections.")
        else:
            st.error(f"OpenAI API error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        return None

def display_analysis_results(analysis: Dict[str, Any]):
    """Display the analysis results in a user-friendly format"""
    
    # Show truncation warning if present
    if 'truncation_warning' in analysis:
        st.warning(f"⚠️ {analysis['truncation_warning']}")
    
    # Overall Score
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Overall Quality Score", f"{analysis['overall_score']}/10")
    with col2:
        st.write("**Overall Assessment:**")
        st.write(analysis['overall_assessment'])
    
    st.divider()
    
    # Criteria Analysis
    st.subheader("📋 Detailed Criteria Analysis")
    
    for i, criterion_analysis in enumerate(analysis['criteria_analysis']):
        with st.expander(f"Criterion {i+1}: {criterion_analysis['criterion']} (Score: {criterion_analysis['score']}/10)"):
            st.write("**Assessment:**")
            st.write(criterion_analysis['assessment'])
            
            if criterion_analysis['issues_found']:
                st.write("**Issues Found:**")
                for issue in criterion_analysis['issues_found']:
                    st.write(f"• {issue}")
            
            if criterion_analysis['recommendations']:
                st.write("**Recommendations:**")
                for rec in criterion_analysis['recommendations']:
                    st.write(f"• {rec}")
    
    st.divider()
    
    # Summary
    st.subheader("📊 Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**✅ Strengths:**")
        for strength in analysis['summary']['strengths']:
            st.write(f"• {strength}")
    
    with col2:
        st.write("**⚠️ Weaknesses:**")
        for weakness in analysis['summary']['weaknesses']:
            st.write(f"• {weakness}")
    
    with col3:
        st.write("**🎯 Priority Improvements:**")
        for improvement in analysis['summary']['priority_improvements']:
            st.write(f"• {improvement}")

def main():
    st.title("📄 Document Quality Control System")
    st.markdown("Upload your documents and define quality criteria to get comprehensive quality analysis powered by AI.")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if api_key:
            st.success("API Key configured ✅")
        else:
            st.warning("Please enter your OpenAI API key to proceed")
        
        st.divider()
        
        st.header("ℹ️ About")
        st.markdown("""
        This tool helps you perform quality control on documents by:
        - Analyzing documents against custom criteria
        - Providing detailed feedback and scores
        - Suggesting improvements
        - Supporting PDF, DOCX, and TXT files
        """)
    
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
        return
    
    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Document")
        
        # File size limit info
        st.info(f"ℹ️ Maximum file size: {MAX_FILE_SIZE_MB} MB")
        
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'docx', 'txt'],
            help=f"Upload PDF, DOCX, or TXT files for quality analysis (max {MAX_FILE_SIZE_MB} MB)"
        )
        
        if uploaded_file:
            # Check file size
            if uploaded_file.size > MAX_FILE_SIZE_BYTES:
                st.error(f"❌ File size ({uploaded_file.size / 1024 / 1024:.1f} MB) exceeds the maximum allowed size of {MAX_FILE_SIZE_MB} MB. Please upload a smaller file.")
                uploaded_file = None
            else:
                st.success(f"File uploaded: {uploaded_file.name}")
                
                # Display file info
                file_details = {
                    "Filename": uploaded_file.name,
                    "File size": f"{uploaded_file.size / 1024:.1f} KB" if uploaded_file.size < 1024*1024 else f"{uploaded_file.size / 1024 / 1024:.1f} MB",
                    "File type": uploaded_file.type
                }
                st.json(file_details)
    
    with col2:
        st.subheader("📝 Quality Assurance Criteria")
        
        # Predefined criteria suggestions
        st.markdown("**Suggested criteria (click to add):**")
        suggested_criteria = [
            "Grammar and spelling accuracy",
            "Clarity and readability",
            "Logical structure and organization",
            "Completeness of information",
            "Professional tone and style",
            "Consistency in formatting",
            "Factual accuracy",
            "Appropriate use of technical terms"
        ]
        
        # Initialize session state for criteria
        if 'qa_criteria' not in st.session_state:
            st.session_state.qa_criteria = []
        
        # Display suggested criteria as buttons
        cols = st.columns(2)
        for i, criterion in enumerate(suggested_criteria):
            with cols[i % 2]:
                if st.button(f"+ {criterion}", key=f"suggest_{i}"):
                    if criterion not in st.session_state.qa_criteria:
                        st.session_state.qa_criteria.append(criterion)
        
        st.divider()
        
        # Custom criteria input
        custom_criterion = st.text_input("Add custom criterion:")
        if st.button("Add Custom Criterion") and custom_criterion:
            if custom_criterion not in st.session_state.qa_criteria:
                st.session_state.qa_criteria.append(custom_criterion)
                st.success(f"Added: {custom_criterion}")
        
        # Display current criteria
        if st.session_state.qa_criteria:
            st.write("**Current QA Criteria:**")
            for i, criterion in enumerate(st.session_state.qa_criteria):
                col_text, col_remove = st.columns([4, 1])
                with col_text:
                    st.write(f"{i+1}. {criterion}")
                with col_remove:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.qa_criteria.pop(i)
                        st.experimental_rerun()
    
    st.divider()
    
    # Analysis section
    if uploaded_file and st.session_state.qa_criteria:
        if st.button("🔍 Analyze Document Quality", type="primary"):
            with st.spinner("Analyzing document quality..."):
                # Extract text based on file type
                document_text = None
                
                if uploaded_file.type == "application/pdf":
                    document_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    document_text = extract_text_from_docx(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    document_text = extract_text_from_txt(uploaded_file)
                
                if document_text:
                    # Check if document is empty
                    if len(document_text.strip()) == 0:
                        st.error("The document appears to be empty. Please upload a document with content.")
                    else:
                        # Show document size info
                        doc_length = len(document_text)
                        st.info(f"📊 Document length: {doc_length:,} characters")
                        
                        if doc_length > MAX_CHARS:
                            st.warning(f"⚠️ Document exceeds {MAX_CHARS:,} characters. It will be truncated for analysis.")
                        
                        # Perform quality analysis
                        analysis = analyze_document_quality(client, document_text, st.session_state.qa_criteria)
                        
                        if analysis:
                            st.success("Analysis completed! 🎉")
                            st.divider()
                            display_analysis_results(analysis)
                        else:
                            st.error("Failed to analyze document. Please try again with a smaller document.")
                else:
                    st.error("Failed to extract text from the document.")
    
    elif uploaded_file and not st.session_state.qa_criteria:
        st.info("📝 Please add some quality assurance criteria to analyze the document.")
    elif not uploaded_file and st.session_state.qa_criteria:
        st.info("📤 Please upload a document to analyze.")
    else:
        st.info("📤 Upload a document and 📝 add quality criteria to get started.")

if __name__ == "__main__":
    main()