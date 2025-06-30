import os
import streamlit as st
from supertrader.trading.engine import TradingEngine, Mode

st.title("Supertrader Dashboard")

api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")

mode = st.sidebar.selectbox("Mode", options=[Mode.LIVE, Mode.PAPER, Mode.BACKTEST])

symbols = st.sidebar.text_input("Symbols", value="BTCUSDT").split(",")
run = st.button("Start")

if run:
    engine = TradingEngine(api_key, api_secret, mode)
    st.write("Engine starting in", mode.value, "mode")
    st.write("Streaming", symbols)
    st.session_state['engine'] = engine
    st.stop()
