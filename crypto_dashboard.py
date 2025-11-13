import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Live Crypto Dashboard",
    page_icon="🪙",
    layout="wide"
)

st.title("🪙 Live Crypto Price Dashboard")
st.markdown(f"Data sourced from [CoinGecko](https://www.coingecko.com/) | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- API Calls & Data Functions ---
# We cache the data for 5 minutes to avoid hitting the API on every refresh
@st.cache_data(ttl=300)
def get_live_prices():
    """Gets live prices for Bitcoin and Ethereum."""
    price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(price_url, timeout=5)
        response.raise_for_status() # Raises an error for bad responses
        data = response.json()
        return data
    except requests.RequestException as e:
        st.error(f"Error fetching live prices: {e}")
        return None

@st.cache_data(ttl=300)
def get_historical_data(coin_id="ethereum", days=7):
    """Gets historical chart data for a given coin."""
    chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    try:
        response = requests.get(chart_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Process the data into a DataFrame
        price_data = data['prices']
        df = pd.DataFrame(price_data, columns=['timestamp', 'price'])
        
        # Convert timestamp to a readable date
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df = df.set_index('date')
        return df[['price']] # Return only the price column with date as index
        
    except requests.RequestException as e:
        st.error(f"Error fetching historical data: {e}")
        return None

# --- Build The Dashboard ---

# 1. Get Live Price Data
live_data = get_live_prices()

if live_data:
    btc_price = live_data.get('bitcoin', {}).get('usd', 0)
    eth_price = live_data.get('ethereum', {}).get('usd', 0)

    # Create two columns for the metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Bitcoin (USD)", value=f"${btc_price:,.0f}")
    with col2:
        st.metric(label="Ethereum (USD)", value=f"${eth_price:,.0f}")

# 2. Get Historical Data & Chart
st.subheader("Ethereum (7-Day Price Chart)")
df_chart_eth = get_historical_data("ethereum", days=7)

if df_chart_eth is not None and not df_chart_eth.empty:
    st.line_chart(df_chart_eth, use_container_width=True)
else:
    st.warning("Could not load Ethereum chart data.")

# 3. Bonus: Bitcoin Chart
st.subheader("Bitcoin (30-Day Price Chart)")
df_chart_btc = get_historical_data("bitcoin", days=30)

if df_chart_btc is not None and not df_chart_btc.empty:
    st.line_chart(df_chart_btc, use_container_width=True, color="#f7931a") # Bitcoin orange
else:
    st.warning("Could not load Bitcoin chart data.")