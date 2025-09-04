import streamlit as st
import openai
from openai import OpenAI
import io
import PyPDF2
import docx
import pandas as pd
from typing import List, Dict, Any
import json

# Page configuration
st.set_page_config(
    page_title="Document Quality Control",
    page_icon="📄",
    layout="wide"
)

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

def analyze_document_quality(client: OpenAI, document_text: str, qa_criteria: List[str]) -> Dict[str, Any]:
    """Analyze document quality using OpenAI"""
    
    criteria_text = "\n".join([f"- {criterion}" for criterion in qa_criteria])
    
    prompt = f"""
    You are a document quality control specialist. Please analyze the following document against these quality assurance criteria:

    Quality Assurance Criteria:
    {criteria_text}

    Document Text:
    {document_text}

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
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert document quality analyst. Provide detailed, constructive feedback in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse the JSON response
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    except json.JSONDecodeError as e:
        st.error(f"Error parsing AI response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        return None

def display_analysis_results(analysis: Dict[str, Any]):
    """Display the analysis results in a user-friendly format"""
    
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
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files for quality analysis"
        )
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size} bytes",
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
                    # Perform quality analysis
                    analysis = analyze_document_quality(client, document_text, st.session_state.qa_criteria)
                    
                    if analysis:
                        st.success("Analysis completed! 🎉")
                        st.divider()
                        display_analysis_results(analysis)
                    else:
                        st.error("Failed to analyze document. Please try again.")
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