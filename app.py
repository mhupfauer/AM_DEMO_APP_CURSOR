import streamlit as st
import openai
import extract_msg
import tempfile
import os
import pandas as pd
from typing import List, Dict, Tuple
import io

# Page configuration
st.set_page_config(
    page_title="Nachrichten Kategorisierer",
    page_icon="📧",
    layout="wide"
)

def extract_msg_content(uploaded_file) -> str:
    """Extract text content from .msg file"""
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.msg') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Extract message content
        msg = extract_msg.Message(tmp_file_path)
        
        # Combine subject and body
        subject = msg.subject or ""
        body = msg.body or ""
        sender = msg.sender or ""
        
        content = f"Absender: {sender}\nBetreff: {subject}\nInhalt: {body}"
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return content
    
    except Exception as e:
        st.error(f"Fehler beim Lesen der .msg Datei: {str(e)}")
        return ""

def categorize_message(content: str, api_key: str) -> Tuple[str, float]:
    """Categorize message using OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""
        Kategorisiere die folgende Nachricht in eine der beiden Kategorien:
        1. "Reporting anfragen" - Anfragen bezüglich Berichten, Reportings, Analysen, Dashboards
        2. "Steuer anfragen" - Anfragen bezüglich Steuern, Steuerberatung, Steuererklärungen
        
        Nachricht:
        {content}
        
        Antworte nur mit der Kategorie und einer Konfidenz zwischen 0 und 1, getrennt durch ein Komma.
        Format: Kategorie, Konfidenz
        Beispiel: Reporting anfragen, 0.85
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein Experte für die Kategorisierung von Geschäftsnachrichten."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
        # Parse result
        parts = result.split(', ')
        if len(parts) == 2:
            category = parts[0].strip()
            confidence = float(parts[1].strip())
            return category, confidence
        else:
            return "Unbekannt", 0.0
            
    except Exception as e:
        st.error(f"Fehler bei der OpenAI API: {str(e)}")
        return "Fehler", 0.0

def main():
    st.title("📧 Nachrichten Kategorisierer")
    st.markdown("Kategorisiere Nachrichten automatisch in **Reporting anfragen** oder **Steuer anfragen**")
    
    # Sidebar for API key
    st.sidebar.header("⚙️ Konfiguration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password",
        help="Geben Sie Ihren OpenAI API Key ein"
    )
    
    if not api_key:
        st.warning("⚠️ Bitte geben Sie Ihren OpenAI API Key in der Sidebar ein.")
        return
    
    # File upload section
    st.header("📁 Dateien hochladen")
    uploaded_files = st.file_uploader(
        "Ziehen Sie .msg Dateien hierher oder klicken Sie zum Auswählen",
        type=['msg'],
        accept_multiple_files=True,
        help="Unterstützte Formate: .msg (Microsoft Outlook Nachrichten)"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} Datei(en) hochgeladen")
        
        # Process files button
        if st.button("🚀 Nachrichten kategorisieren", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Verarbeite {uploaded_file.name}...")
                
                # Extract content
                content = extract_msg_content(uploaded_file)
                
                if content:
                    # Categorize
                    category, confidence = categorize_message(content, api_key)
                    
                    results.append({
                        "Dateiname": uploaded_file.name,
                        "Kategorie": category,
                        "Konfidenz": f"{confidence:.2f}",
                        "Vorschau": content[:200] + "..." if len(content) > 200 else content
                    })
                else:
                    results.append({
                        "Dateiname": uploaded_file.name,
                        "Kategorie": "Fehler",
                        "Konfidenz": "0.00",
                        "Vorschau": "Fehler beim Lesen der Datei"
                    })
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Verarbeitung abgeschlossen!")
            
            # Display results
            st.header("📊 Ergebnisse")
            
            if results:
                df = pd.DataFrame(results)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                
                reporting_count = len(df[df['Kategorie'] == 'Reporting anfragen'])
                steuer_count = len(df[df['Kategorie'] == 'Steuer anfragen'])
                error_count = len(df[df['Kategorie'].isin(['Fehler', 'Unbekannt'])])
                
                col1.metric("Reporting anfragen", reporting_count)
                col2.metric("Steuer anfragen", steuer_count)
                col3.metric("Fehler/Unbekannt", error_count)
                
                # Results table
                st.subheader("Detaillierte Ergebnisse")
                
                # Color coding for categories
                def highlight_category(val):
                    if val == 'Reporting anfragen':
                        return 'background-color: #e8f4fd'
                    elif val == 'Steuer anfragen':
                        return 'background-color: #fff2e8'
                    elif val in ['Fehler', 'Unbekannt']:
                        return 'background-color: #ffeaea'
                    return ''
                
                styled_df = df.style.applymap(highlight_category, subset=['Kategorie'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Download results
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Ergebnisse als CSV herunterladen",
                    data=csv,
                    file_name="kategorisierung_ergebnisse.csv",
                    mime="text/csv"
                )
    
    # Instructions
    with st.expander("ℹ️ Anweisungen"):
        st.markdown("""
        ### So verwenden Sie die Anwendung:
        
        1. **API Key eingeben**: Geben Sie Ihren OpenAI API Key in der Sidebar ein
        2. **Dateien hochladen**: Ziehen Sie .msg Dateien in den Upload-Bereich oder klicken Sie zum Auswählen
        3. **Kategorisieren**: Klicken Sie auf "Nachrichten kategorisieren" um die Verarbeitung zu starten
        4. **Ergebnisse ansehen**: Die Kategorisierung wird in einer Tabelle angezeigt
        5. **Herunterladen**: Laden Sie die Ergebnisse als CSV-Datei herunter
        
        ### Kategorien:
        - **Reporting anfragen**: Anfragen bezüglich Berichten, Reportings, Analysen, Dashboards
        - **Steuer anfragen**: Anfragen bezüglich Steuern, Steuerberatung, Steuererklärungen
        
        ### Unterstützte Dateiformate:
        - .msg (Microsoft Outlook Nachrichten)
        """)

if __name__ == "__main__":
    main()