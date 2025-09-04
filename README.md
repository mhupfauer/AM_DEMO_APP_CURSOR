# Nachrichten Kategorisierer

Eine Webanwendung zur automatischen Kategorisierung von .msg-Dateien in "Reporting anfragen" und "Steuer anfragen" mit Hilfe von OpenAI.

## Features

- **Drag & Drop Upload**: Einfaches Hochladen von .msg-Dateien per Drag & Drop
- **OpenAI Integration**: Intelligente Kategorisierung mit GPT-3.5-turbo
- **Moderne UI**: Responsive und benutzerfreundliche Oberfläche
- **Batch-Verarbeitung**: Mehrere Dateien gleichzeitig verarbeiten
- **Konfidenz-Anzeige**: Vertrauenswert für jede Kategorisierung
- **Inhalts-Vorschau**: Vorschau des analysierten Nachrichteninhalts

## Kategorien

- **Reporting anfragen**: Nachrichten zu Berichten, Reportings, Analysen, Dashboards, KPIs, Metriken
- **Steuer anfragen**: Nachrichten zu Steuern, Steuerberatung, Steuererklärungen, Steuerrecht

## Installation und Start

### Voraussetzungen
- Python 3.8 oder höher
- OpenAI API Key

### Schnellstart
```bash
# Abhängigkeiten installieren und Server starten
./start.sh
```

### Manuelle Installation
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
python main.py
```

Die Anwendung ist dann unter http://localhost:8000 erreichbar.

## Verwendung

1. **API Key eingeben**: Geben Sie Ihren OpenAI API Key in das entsprechende Feld ein
2. **Dateien hochladen**: Ziehen Sie .msg-Dateien in den Upload-Bereich oder klicken Sie zum Auswählen
3. **Kategorisierung starten**: Klicken Sie auf "Nachrichten kategorisieren"
4. **Ergebnisse ansehen**: Die kategorisierten Nachrichten werden mit Konfidenzwerten angezeigt

## API Endpoints

### POST /categorize
Kategorisiert hochgeladene .msg-Dateien.

**Parameter:**
- `api_key` (Form): OpenAI API Key
- `files` (Files): Liste von .msg-Dateien

**Response:**
```json
[
  {
    "filename": "nachricht.msg",
    "category": "Reporting anfragen",
    "confidence": 0.85,
    "content_preview": "Subject: Quartals-Report..."
  }
]
```

## Technische Details

- **Backend**: FastAPI mit Python
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Message Parsing**: extract-msg Library
- **AI Model**: OpenAI GPT-3.5-turbo
- **File Support**: Microsoft Outlook .msg Format

## Abhängigkeiten

- fastapi==0.104.1
- uvicorn==0.24.0
- python-multipart==0.0.6
- openai==1.3.7
- extract-msg==0.48.4
- python-magic==0.4.27
- pydantic==2.5.0

## Sicherheitshinweise

- Der API Key wird nur für die aktuelle Session gespeichert
- Hochgeladene Dateien werden nach der Verarbeitung automatisch gelöscht
- Keine persistente Speicherung von Nachrichten oder API Keys