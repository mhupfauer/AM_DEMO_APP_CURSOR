# Document Quality Control System

A Streamlit application that performs quality control analysis on uploaded documents using OpenAI's GPT-4 model.

## Features

- **Multi-format Support**: Upload PDF, DOCX, or TXT files
- **Custom Quality Criteria**: Define your own quality assurance criteria or use suggested ones
- **AI-Powered Analysis**: Uses OpenAI GPT-4 for comprehensive document analysis
- **Detailed Reporting**: Get scores, assessments, and actionable recommendations
- **User-Friendly Interface**: Clean, intuitive Streamlit interface

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (usually `http://localhost:8501`)

3. Enter your OpenAI API key in the sidebar

4. Upload a document (PDF, DOCX, or TXT)

5. Add quality assurance criteria:
   - Use suggested criteria by clicking the buttons
   - Add custom criteria using the text input

6. Click "Analyze Document Quality" to get your analysis

## Quality Analysis Features

The system provides:
- **Overall Quality Score** (1-10)
- **Detailed Criteria Analysis** with individual scores and assessments
- **Issue Identification** with specific problems found
- **Actionable Recommendations** for improvement
- **Summary Report** with strengths, weaknesses, and priority improvements

## Supported File Types

- **PDF**: Extracts text from all pages
- **DOCX**: Extracts text from Word documents
- **TXT**: Reads plain text files

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls

## Dependencies

See `requirements.txt` for the full list of dependencies.

## Configuration

The app requires an OpenAI API key, which should be entered in the sidebar. The key is used to access GPT-4 for document analysis.

## Example Quality Criteria

- Grammar and spelling accuracy
- Clarity and readability
- Logical structure and organization
- Completeness of information
- Professional tone and style
- Consistency in formatting
- Factual accuracy
- Appropriate use of technical terms

## Note

This application uses OpenAI's API, which may incur costs based on usage. Please refer to OpenAI's pricing for more information.