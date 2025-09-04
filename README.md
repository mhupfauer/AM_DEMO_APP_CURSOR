# German Stock Market Tracker

A comprehensive Streamlit application for tracking German stocks and ETFs with AI-powered chat analysis using OpenAI.

## Features

- 📈 Real-time German stock market data (DAX companies and ETFs)
- 📊 Interactive charts and visualizations using Plotly
- 💬 AI-powered chat interface for data analysis
- 🔍 Performance comparison across multiple stocks
- 📋 Detailed stock information and metrics
- ⚡ Cached data fetching for improved performance

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Configure the application:
   - Enter your OpenAI API key in the sidebar to enable chat features
   - Select stocks from the available German companies and ETFs
   - Choose your preferred time period for analysis

## Getting an OpenAI API Key

To use the chat features, you'll need an OpenAI API key:

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy and paste it into the sidebar of the application

## Supported Stocks

### DAX Companies
- SAP SE
- ASML Holding
- Siemens AG
- Allianz SE
- Deutsche Telekom AG
- Mercedes-Benz Group AG
- BMW AG
- BASF SE
- Volkswagen AG
- Adidas AG
- Deutsche Post AG
- Munich Re
- Beiersdorf AG
- Henkel AG & Co. KGaA
- Continental AG

### German ETFs
- iShares Core DAX UCITS ETF
- Xtrackers MSCI World UCITS ETF
- Xtrackers MSCI Europe UCITS ETF
- Xtrackers DAX UCITS ETF

## Features Overview

### Market Data Visualization
- Performance comparison charts
- Real-time price tables
- Detailed candlestick charts
- Volume analysis
- Historical data analysis

### AI Chat Assistant
- Ask questions about stock performance
- Get investment insights (educational purposes)
- Analyze market trends
- Compare different stocks
- Understand market movements

## Technical Details

- **Data Source**: Yahoo Finance API via yfinance
- **Visualization**: Plotly for interactive charts
- **AI Backend**: OpenAI GPT-3.5-turbo
- **Caching**: Streamlit's built-in caching for performance
- **UI Framework**: Streamlit with responsive design

## Example Questions for the AI Chat

- "Which stocks performed best today?"
- "What's the trend for SAP over the last month?"
- "Should I be concerned about the recent drop in BMW stock?"
- "Compare the performance of automotive stocks"
- "What factors might be affecting Siemens' stock price?"

## Requirements

- Python 3.8+
- Internet connection for real-time data
- OpenAI API key for chat features

## License

This project is for educational and personal use. Please ensure compliance with data provider terms of service and financial regulations in your jurisdiction.

## Disclaimer

This application is for educational purposes only. The information provided should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.