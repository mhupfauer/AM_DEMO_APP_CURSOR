from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import openai
import extract_msg
import io
import os
from typing import List, Optional
from pydantic import BaseModel
import tempfile

app = FastAPI(title="Message Categorizer", description="Categorize messages into Reporting or Steuer anfragen")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class CategoryResponse(BaseModel):
    filename: str
    category: str
    confidence: float
    content_preview: str

class CategorizeRequest(BaseModel):
    api_key: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/categorize", response_model=List[CategoryResponse])
async def categorize_messages(
    api_key: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Categorize uploaded .msg files"""
    if not api_key:
        raise HTTPException(status_code=400, detail="OpenAI API key is required")
    
    # Set OpenAI client
    openai_client = openai.OpenAI(api_key=api_key)
    
    results = []
    
    for file in files:
        try:
            # Validate file type
            if not file.filename.lower().endswith('.msg'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} is not a .msg file")
            
            # Read file content
            content = await file.read()
            
            # Parse .msg file
            with tempfile.NamedTemporaryFile(suffix='.msg', delete=False) as tmp_file:
                tmp_file.write(content)
                tmp_file.flush()
                
                try:
                    msg = extract_msg.Message(tmp_file.name)
                    
                    # Extract message content
                    subject = msg.subject or ""
                    body = msg.body or ""
                    sender = msg.sender or ""
                    
                    # Combine content for analysis
                    message_content = f"Subject: {subject}\nFrom: {sender}\nBody: {body}"
                    
                    # Categorize using OpenAI
                    category, confidence = await categorize_with_openai(message_content, openai_client)
                    
                    # Create preview (first 200 characters)
                    preview = message_content[:200] + "..." if len(message_content) > 200 else message_content
                    
                    results.append(CategoryResponse(
                        filename=file.filename,
                        category=category,
                        confidence=confidence,
                        content_preview=preview
                    ))
                    
                finally:
                    # Clean up temporary file
                    os.unlink(tmp_file.name)
                    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
    
    return results

async def categorize_with_openai(content: str, openai_client) -> tuple[str, float]:
    """Use OpenAI to categorize the message content"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Du bist ein Experte für die Kategorisierung von Geschäftsnachrichten. 
                    Deine Aufgabe ist es, Nachrichten in eine der folgenden Kategorien einzuteilen:
                    
                    1. "Reporting anfragen" - Nachrichten die sich auf Berichte, Reportings, Analysen, 
                       Dashboards, KPIs, Metriken oder ähnliche Berichterstattung beziehen.
                    
                    2. "Steuer anfragen" - Nachrichten die sich auf Steuern, Steuerberatung, 
                       Steuererklärungen, Steuerrecht oder steuerliche Angelegenheiten beziehen.
                    
                    Antworte nur mit der Kategorie und einem Konfidenzwert zwischen 0 und 1, 
                    getrennt durch ein Pipe-Symbol (|). Beispiel: "Reporting anfragen|0.85"
                    """
                },
                {
                    "role": "user",
                    "content": f"Kategorisiere diese Nachricht:\n\n{content}"
                }
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
        # Parse result
        parts = result.split("|")
        if len(parts) == 2:
            category = parts[0].strip()
            confidence = float(parts[1].strip())
        else:
            # Fallback if format is unexpected
            category = "Reporting anfragen" if "reporting" in result.lower() else "Steuer anfragen"
            confidence = 0.5
        
        return category, confidence
        
    except Exception as e:
        # Fallback categorization
        content_lower = content.lower()
        if any(word in content_lower for word in ['steuer', 'tax', 'abgabe', 'finanzamt']):
            return "Steuer anfragen", 0.6
        else:
            return "Reporting anfragen", 0.6

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)