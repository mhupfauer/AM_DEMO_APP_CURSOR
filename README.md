# Nachrichten Kategorisierer

Eine Streamlit-Anwendung zur automatischen Kategorisierung von E-Mail-Nachrichten in "Reporting anfragen" und "Steuer anfragen" unter Verwendung von OpenAI.

## Features

- 📧 Drag-and-Drop Upload für .msg Dateien (Microsoft Outlook)
- 🤖 Automatische Kategorisierung mit OpenAI GPT-3.5-turbo
- 📊 Übersichtliche Darstellung der Ergebnisse
- 📥 CSV-Export der Kategorisierungsergebnisse
- 🔒 Sichere API-Key-Eingabe über die Sidebar

## Installation

1. Klonen Sie das Repository oder laden Sie die Dateien herunter
2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

## Verwendung

1. Starten Sie die Anwendung:
   ```bash
   streamlit run app.py
   ```

2. Öffnen Sie Ihren Browser und gehen Sie zu `http://localhost:8501`

3. Geben Sie Ihren OpenAI API Key in der Sidebar ein

4. Laden Sie .msg Dateien per Drag-and-Drop hoch

5. Klicken Sie auf "Nachrichten kategorisieren"

6. Sehen Sie sich die Ergebnisse an und laden Sie sie als CSV herunter

## Kategorien

- **Reporting anfragen**: Anfragen bezüglich Berichten, Reportings, Analysen, Dashboards
- **Steuer anfragen**: Anfragen bezüglich Steuern, Steuerberatung, Steuererklärungen

## Technische Details

- **Frontend**: Streamlit
- **Backend**: OpenAI GPT-3.5-turbo
- **Dateiformate**: .msg (Microsoft Outlook Nachrichten)
- **Ausgabe**: Kategorisierung mit Konfidenzwert

## Abhängigkeiten

- streamlit==1.29.0
- openai==1.6.1
- extract-msg==0.47.0
- python-magic==0.4.27
- pandas==2.1.4

## Hinweise

- Ein gültiger OpenAI API Key ist erforderlich
- Die Anwendung verarbeitet nur .msg Dateien
- Alle hochgeladenen Dateien werden temporär verarbeitet und nicht gespeichert