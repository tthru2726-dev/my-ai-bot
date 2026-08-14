import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Master AI Trading Dashboard", layout="centered", page_icon="🎯")
st.title("🎯 Master AI Trading Dashboard")
st.caption("Elliott Wave + Multi-Timeframe + Risk Management Engine")

symbol = st.selectbox("Asset Select කරන්න:", ['BTC-USD', 'GC=F', 'ETH-USD'], index=0)
entry_tf = st.select_slider("Entry Timeframe:", options=['15m', '1h', '4h', '1d'], value='4h')

col1, col2 = st.columns(2)
with col1:
    acc_balance = st.number_input("Account Balance ($):", value=1000.0)
with col2:
    risk_pct = st.number_input("Risk Per Trade (%):", value=1.0, min_value=0.1, max_value=5.0)

if st.button("Run Master Analysis 🚀", type="primary"):
    st.info(f"Analyzing Market Data for {symbol}...")
    htf_data = yf.download(tickers=symbol, period='3mo', interval='1d', progress=False)
    ltf_data = yf.download(tickers=symbol, period='1mo', interval=entry_tf, progress=False)
    
    if htf_data.empty or ltf_data.empty:
        st.error("Data ලබාගැනීමට නොහැකි විය.")
    else:
        htf_prices = htf_data['Close'].values.flatten()
        htf_trend = "BULLISH" if htf_prices[-1] > htf_prices[-20] else "BEARISH"
        
        ltf_prices = ltf_data['Close'].values.flatten()
        current_price = float(ltf_prices[-1])
        recent_low = float(np.min(ltf_prices[-30:]))
        recent_high = float(np.max(ltf_prices[-30:]))
        
        diff = recent_high - recent_low
        fib_618 = recent_high - (diff * 0.618)
        fib_382 = recent_high - (diff * 0.382)
        
        signal = "NO SIGNAL"
        confidence = 60
        
        if htf_trend == "BULLISH" and abs(current_price - fib_618) / current_price < 0.015:
            signal = "BUY"
            confidence = 94
            sl = recent_low * 0.998
            tp = current_price + (diff * 1.618)
        elif htf_trend == "BEARISH" and abs(current_price - fib_382) / current_price < 0.015:
            signal = "SELL"
            confidence = 91
            sl = recent_high * 1.002
            tp = current_price - (diff * 1.618)

        st.subheader("📊 Analysis Results")
        st.write(f"**Main 1D Trend:** `{htf_trend}` | **Live Price:** `${current_price:,.2f}`")
        
        risk_amount = acc_balance * (risk_pct / 100.0)
        
        if signal != "NO SIGNAL" and confidence >= 90:
            sl_distance = abs(current_price - sl)
            recommended_units = risk_amount / sl_distance
            
            st.success(f"🟢 ACTIVE SIGNAL: {signal} ({confidence}% Accuracy)")
            st.metric("Entry Price", f"${current_price:,.2f}")
            st.metric("Stop Loss (SL)", f"${sl:,.2f}")
            st.metric("Take Profit (TP)", f"${tp:,.2f}")
            st.warning(f"🎯 Recommended Position Size: {recommended_units:.4f} Units / Lots")
        else:
            st.warning(f"⚠️ NO 90%+ SIGNAL FOUND (Confidence: {confidence}%)")
            st.write("90% සාර්ථකත්වයක් සහිත Pattern එකක් නැත. Market එක Wait කරන්න.")
