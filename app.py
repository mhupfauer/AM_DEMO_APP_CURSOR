import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import openai
import json
from typing import List, Dict, Any
import numpy as np

# Page configuration
st.set_page_config(
    page_title="German Stock Market Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# German stock symbols and ETFs
GERMAN_STOCKS = {
    "DAX Companies": {
        "SAP.DE": "SAP SE",
        "ASME.DE": "ASML Holding",
        "SIE.DE": "Siemens AG",
        "ALV.DE": "Allianz SE",
        "DTE.DE": "Deutsche Telekom AG",
        "MBG.DE": "Mercedes-Benz Group AG",
        "BMW.DE": "Bayerische Motoren Werke AG",
        "BAS.DE": "BASF SE",
        "VOW3.DE": "Volkswagen AG",
        "ADS.DE": "Adidas AG",
        "DHL.DE": "Deutsche Post AG",
        "MUV2.DE": "Munich Re",
        "BEI.DE": "Beiersdorf AG",
        "HEN3.DE": "Henkel AG & Co. KGaA",
        "CON.DE": "Continental AG"
    },
    "German ETFs": {
        "EXS1.DE": "iShares Core DAX UCITS ETF",
        "XMME.DE": "Xtrackers MSCI World UCITS ETF",
        "XMEU.DE": "Xtrackers MSCI Europe UCITS ETF",
        "DBXD.DE": "Xtrackers DAX UCITS ETF"
    }
}

class StockDataManager:
    def __init__(self):
        self.cache_duration = 300  # 5 minutes
        
    @st.cache_data(ttl=300)
    def get_stock_data(_self, symbol: str, period: str = "1d") -> pd.DataFrame:
        """Fetch stock data with caching"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def get_multiple_stocks(_self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Fetch current data for multiple stocks"""
        results = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
                    
                    results[symbol] = {
                        'name': info.get('longName', symbol),
                        'price': current_price,
                        'change': change,
                        'change_pct': change_pct,
                        'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0,
                        'market_cap': info.get('marketCap', 'N/A')
                    }
            except Exception as e:
                st.warning(f"Could not fetch data for {symbol}: {str(e)}")
                
        return results

class ChatInterface:
    def __init__(self, api_key: str):
        if api_key:
            openai.api_key = api_key
            self.client = openai.OpenAI(api_key=api_key)
        else:
            self.client = None
    
    def analyze_stock_data(self, stock_data: Dict[str, Any], user_question: str) -> str:
        """Analyze stock data using OpenAI"""
        if not self.client:
            return "Please provide an OpenAI API key to use the chat feature."
        
        # Prepare data summary for the AI
        data_summary = self._prepare_data_summary(stock_data)
        
        system_prompt = """You are a financial analyst AI assistant specializing in German stock market data. 
        You have access to real-time stock data and can provide insights, analysis, and answer questions about:
        - Stock prices and performance
        - Market trends
        - Company information
        - Investment recommendations (educational purposes only)
        
        Always base your responses on the provided data and be clear about limitations.
        Provide actionable insights when possible."""
        
        user_prompt = f"""
        Current German stock market data:
        {data_summary}
        
        User question: {user_question}
        
        Please provide a comprehensive analysis based on this data.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _prepare_data_summary(self, stock_data: Dict[str, Any]) -> str:
        """Prepare a summary of stock data for the AI"""
        summary_parts = []
        
        for symbol, data in stock_data.items():
            if isinstance(data, dict):
                summary_parts.append(
                    f"{data.get('name', symbol)} ({symbol}): "
                    f"Price: €{data.get('price', 0):.2f}, "
                    f"Change: {data.get('change_pct', 0):+.2f}%, "
                    f"Volume: {data.get('volume', 0):,}"
                )
        
        return "\n".join(summary_parts)

def create_price_chart(data: pd.DataFrame, title: str) -> go.Figure:
    """Create an interactive price chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="Price"
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Price (EUR)",
        xaxis_title="Date",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_volume_chart(data: pd.DataFrame, title: str) -> go.Figure:
    """Create a volume chart"""
    fig = go.Figure()
    
    colors = ['red' if close < open else 'green' 
             for close, open in zip(data['Close'], data['Open'])]
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name="Volume",
        marker_color=colors
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Volume",
        xaxis_title="Date",
        template="plotly_white",
        height=300
    )
    
    return fig

def create_performance_comparison(stock_data: Dict[str, Any]) -> go.Figure:
    """Create a performance comparison chart"""
    symbols = list(stock_data.keys())
    changes = [stock_data[symbol].get('change_pct', 0) for symbol in symbols]
    names = [stock_data[symbol].get('name', symbol)[:20] + '...' 
             if len(stock_data[symbol].get('name', symbol)) > 20 
             else stock_data[symbol].get('name', symbol) for symbol in symbols]
    
    colors = ['green' if change >= 0 else 'red' for change in changes]
    
    fig = go.Figure(data=[
        go.Bar(x=names, y=changes, marker_color=colors)
    ])
    
    fig.update_layout(
        title="Daily Performance Comparison",
        yaxis_title="Change (%)",
        xaxis_title="Stocks",
        template="plotly_white",
        height=400,
        xaxis={'tickangle': -45}
    )
    
    return fig

def main():
    st.title("📈 German Stock Market Tracker")
    st.markdown("Track German stocks and ETFs with AI-powered analysis")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # OpenAI API Key input
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key to enable chat features"
    )
    
    # Stock selection
    st.sidebar.header("Stock Selection")
    selected_category = st.sidebar.selectbox(
        "Select Category",
        list(GERMAN_STOCKS.keys())
    )
    
    available_stocks = GERMAN_STOCKS[selected_category]
    selected_stocks = st.sidebar.multiselect(
        "Select Stocks",
        options=list(available_stocks.keys()),
        default=list(available_stocks.keys())[:5],
        format_func=lambda x: f"{available_stocks[x]} ({x})"
    )
    
    # Time period selection
    period = st.sidebar.selectbox(
        "Time Period",
        ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
        index=2
    )
    
    # Initialize managers
    stock_manager = StockDataManager()
    chat_interface = ChatInterface(api_key) if api_key else None
    
    # Main layout - split view
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Market Data")
        
        if selected_stocks:
            # Fetch current stock data
            with st.spinner("Fetching stock data..."):
                current_data = stock_manager.get_multiple_stocks(selected_stocks)
            
            if current_data:
                # Performance comparison
                st.subheader("Performance Overview")
                perf_chart = create_performance_comparison(current_data)
                st.plotly_chart(perf_chart, use_container_width=True)
                
                # Stock table
                st.subheader("Current Prices")
                table_data = []
                for symbol, data in current_data.items():
                    table_data.append({
                        "Symbol": symbol,
                        "Name": data.get('name', symbol),
                        "Price (€)": f"{data.get('price', 0):.2f}",
                        "Change (€)": f"{data.get('change', 0):+.2f}",
                        "Change (%)": f"{data.get('change_pct', 0):+.2f}%",
                        "Volume": f"{data.get('volume', 0):,}"
                    })
                
                df_table = pd.DataFrame(table_data)
                st.dataframe(df_table, use_container_width=True)
                
                # Detailed charts for selected stock
                st.subheader("Detailed Analysis")
                chart_stock = st.selectbox(
                    "Select stock for detailed chart",
                    selected_stocks,
                    format_func=lambda x: f"{available_stocks[x]} ({x})"
                )
                
                if chart_stock:
                    with st.spinner(f"Loading detailed data for {chart_stock}..."):
                        detailed_data = stock_manager.get_stock_data(chart_stock, period)
                    
                    if not detailed_data.empty:
                        # Price chart
                        price_chart = create_price_chart(
                            detailed_data, 
                            f"{available_stocks[chart_stock]} ({chart_stock}) - Price"
                        )
                        st.plotly_chart(price_chart, use_container_width=True)
                        
                        # Volume chart
                        if 'Volume' in detailed_data.columns:
                            volume_chart = create_volume_chart(
                                detailed_data,
                                f"{available_stocks[chart_stock]} ({chart_stock}) - Volume"
                            )
                            st.plotly_chart(volume_chart, use_container_width=True)
        else:
            st.info("Please select at least one stock from the sidebar.")
    
    with col2:
        st.header("💬 AI Chat Assistant")
        
        if not api_key:
            st.warning("Please enter your OpenAI API key in the sidebar to enable chat features.")
            st.info("""
            To get an OpenAI API key:
            1. Go to https://platform.openai.com/
            2. Sign up or log in
            3. Navigate to API Keys section
            4. Create a new API key
            5. Paste it in the sidebar
            """)
        else:
            st.success("Chat enabled! Ask questions about the stock data.")
            
            # Chat interface
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask about the stock data..."):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Generate AI response
                if selected_stocks and current_data:
                    with st.chat_message("assistant"):
                        with st.spinner("Analyzing..."):
                            response = chat_interface.analyze_stock_data(current_data, prompt)
                        st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    with st.chat_message("assistant"):
                        st.markdown("Please select some stocks first to analyze the data.")
            
            # Clear chat button
            if st.button("Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Tips**: Select stocks from the sidebar, choose a time period, and ask the AI assistant questions about trends, performance, or investment insights!"
    )

if __name__ == "__main__":
    main()