# Portfolio Project 4: Live Crypto Dashboard

This is a live data dashboard built in Python using Streamlit, Pandas, and the CoinGecko API.

## Features

* **Live Data:** Connects to a public API (`requests`) to pull live prices for Bitcoin and Ethereum.
* **Dynamic Metrics:** Displays live prices using `st.metric`.
* **Historical Charting:** Fetches 7-day (Ethereum) and 30-day (Bitcoin) historical data, processes it with `pandas`, and visualizes it with `st.line_chart`.
* **Data Caching:** Uses `st.cache_data(ttl=300)` to cache API results for 5 minutes, ensuring a fast user experience and respecting API rate limits.