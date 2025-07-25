# screener_app.py
# టెర్మినల్‌లో 'streamlit run screener_app.py' తో రన్ చేయండి

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
import requests

# --- పేజ్ సెటప్ ---
st.set_page_config(layout="wide", page_title="Stock Screener & Analyzer")

# --- హెల్పర్ ఫంక్షన్లు (పైన ఉన్న స్క్రిప్ట్ నుండి కాపీ చేయబడినవి) ---
# ఈ ఫంక్షన్లు మార్పు లేకుండా ఇక్కడ అవసరం
def clean_data(df):
    if df.empty: return df
    df = df[df.index <= pd.to_datetime('today').normalize()]
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    df = df.loc[:,~df.columns.duplicated()]
    ohlcv = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=ohlcv, inplace=True)
    return df

def wma(series, length):
    weights = np.arange(1, length + 1)
    return series.rolling(length).apply(lambda p: np.dot(p, weights) / weights.sum(), raw=True)

def hma(series, length):
    half_len, sqrt_len = int(length / 2), int(np.sqrt(length))
    return wma(2 * wma(series, half_len) - wma(series, length), sqrt_len)

def compute_atr(high, low, close, period):
    tr = pd.concat([high - low, abs(high - close.shift(1)), abs(low - close.shift(1))], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False).mean()

def compute_rsi(series, period):
    delta = series.diff(1); gain = delta.where(delta > 0, 0); loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_macd(series, fast, slow, signal):
    exp1 = series.ewm(span=fast, adjust=False).mean(); exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2; signal_line = macd.ewm(span=signal, adjust=False).mean(); hist = macd - signal_line
    return macd, signal_line, hist

def add_all_indicators(df, config):
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['Change %'] = df['Close'].pct_change() * 100
    df['RSI14'] = compute_rsi(df['Close'], period=config['RSI_PERIOD'])
    df['RSI_EMA20'] = df['RSI14'].ewm(span=config['RSI_EMA_PERIOD'], adjust=False).mean()
    _, _, df['MACD_Hist'] = compute_macd(df['Close'], config['MACD_FAST'], config['MACD_SLOW'], config['MACD_SIGNAL'])
    atr = compute_atr(df['High'], df['Low'], df['Close'], config['UT_ATR_PERIOD'])
    n_loss = config['UT_SENSITIVITY'] * atr
    atr_ts = pd.Series(np.nan, index=df.index); atr_ts.iloc[0] = 0
    for i in range(1, len(df)):
        cl, prev_cl, prev_ts = df['Close'].iloc[i], df['Close'].iloc[i-1], atr_ts.iloc[i-1]
        if cl > prev_ts and prev_cl > prev_ts: atr_ts.iloc[i] = max(prev_ts, cl - n_loss.iloc[i])
        elif cl < prev_ts and prev_cl < prev_ts: atr_ts.iloc[i] = min(prev_ts, cl + n_loss.iloc[i])
        elif cl > prev_ts: atr_ts.iloc[i] = cl - n_loss.iloc[i]
        else: atr_ts.iloc[i] = cl + n_loss.iloc[i]
    df['ATR_Stop'] = atr_ts
    df['UT_Trend'] = np.where(df['Close'] > df['ATR_Stop'], 1, -1)
    df['HMA'] = hma(df['Close'], config['HMA_PERIOD'])
    df[f'EMA{config["EMA_SHORT"]}'] = df['Close'].ewm(span=config["EMA_SHORT"], adjust=False).mean()
    df[f'EMA{config["EMA_MEDIUM"]}'] = df['Close'].ewm(span=config["EMA_MEDIUM"], adjust=False).mean()
    return df

def apply_trading_logic(df, config):
    ema_golden_cross = (df[f'EMA{config["EMA_SHORT"]}'] > df[f'EMA{config["EMA_MEDIUM"]}']) & (df[f'EMA{config["EMA_SHORT"]}'].shift(1) <= df[f'EMA{config["EMA_MEDIUM"]}'].shift(1))
    buy_signal = (df['UT_Trend'] == 1) & (df['Close'] > df['HMA']) & ema_golden_cross
    df['Signal'] = np.where(buy_signal, "BUY", "-")
    df['Buy_Marker'] = np.where(buy_signal, df['Low'] * 0.985, np.nan)
    return df

def check_scanner_conditions(df):
    if len(df) < 2: return False
    try:
        latest = df.iloc[-1]; previous = df.iloc[-2]
        cond1 = latest['Close'] > latest['EMA9'] and previous['Close'] <= previous['EMA9']
        cond2 = latest['Volume'] > 100000
        cond3 = latest['Change %'] < 10
        cond4 = latest['Close'] > 60
        cond5 = latest['RSI14'] > latest['RSI_EMA20']
        cond6 = latest['MACD_Hist'] > 0 and previous['MACD_Hist'] <= 0
        return cond1 and cond2 and cond3 and cond4 and cond5 and cond6
    except Exception: return False

def run_backtest_with_atr_stop(df, initial_capital=100000):
    df_bt = df.copy().dropna(subset=['ATR_Stop', 'Signal'])
    if df_bt.empty: return "Not enough data for backtest.", None
    capital = initial_capital; position = 0; trades = []
    for i in range(1, len(df_bt)):
        if position == 0 and df_bt['Signal'].iloc[i] == 'BUY':
            entry_price = df_bt['Close'].iloc[i]; entry_date = df_bt.index[i]
            position = 1; shares = capital / entry_price
        elif position == 1 and df_bt['Close'].iloc[i] < df_bt['ATR_Stop'].iloc[i]:
            exit_price = df_bt['Close'].iloc[i]; exit_date = df_bt.index[i]
            position = 0
            pnl = (exit_price - entry_price) * shares; capital += pnl
            trades.append({"EntryDate": entry_date, "EntryPrice": entry_price, "ExitDate": exit_date, "ExitPrice": exit_price, "PnL": pnl})
    if not trades: return "No trades were executed.", None
    results_df = pd.DataFrame(trades)
    total_pnl = results_df['PnL'].sum(); win_rate = (results_df['PnL'] > 0).sum() / len(results_df) * 100
    summary = {
        "Initial Capital": f"₹{initial_capital:,.2f}", "Final Capital": f"₹{capital:,.2f}",
        "Total PnL": f"₹{total_pnl:,.2f} ({(capital/initial_capital - 1)*100:.2f}%)",
        "Total Trades": len(results_df), "Win Rate": f"{win_rate:.2f}%"
    }
    return summary, results_df

# --- STREAMLIT APP ---
st.title("📈 Hybrid Stock Screener & Analyzer")
st.markdown("This app scans NSE stocks based on a bullish crossover strategy and provides detailed analysis with backtesting.")

# --- SIDEBAR FOR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls & Settings")
    
    # Stock List Input
    default_stocks = 'RELIANCE,TCS,HDFCBANK,INFY,ICICIBANK,HINDUNILVR,ITC,SBIN,BAJFINANCE,BHARTIARTL,ASIANPAINT,WIPRO'
    stock_list_input = st.text_area("Enter Stock Symbols (comma-separated)", default_stocks, height=150)
    
    # Configuration
    st.subheader("Indicator Settings")
    ema_short = st.slider("Short EMA Period", 5, 50, 9)
    ema_medium = st.slider("Medium EMA Period", 10, 100, 21)
    data_period = st.selectbox("Data Period for Scan", ["1y", "2y", "5y", "10y"], index=2)
    
    run_button = st.button("🚀 Run Screener")
    
# Build CONFIG dictionary from user inputs
CONFIG = {
    "STOCKS": [s.strip().upper() for s in stock_list_input.split(',')],
    "DATA_PERIOD": data_period, "PLOT_DAYS": 500,
    "UT_SENSITIVITY": 1, "UT_ATR_PERIOD": 99, "HMA_PERIOD": 55,
    "EMA_SHORT": ema_short, "EMA_MEDIUM": ema_medium,
    "RSI_PERIOD": 14, "RSI_EMA_PERIOD": 20,
    "MACD_FAST": 12, "MACD_SLOW": 26, "MACD_SIGNAL": 9,
    "BACKTEST_CAPITAL": 100000,
}

# --- MAIN SCREENER LOGIC (CACHED) ---
@st.cache_data(ttl=3600) # Cache for 1 hour
def run_full_scan(_config):
    passing_stocks_data = {}
    stock_list = _config['STOCKS']
    progress_bar = st.progress(0, "Starting Scan...")
    
    for i, symbol in enumerate(stock_list):
        try:
            progress_bar.progress((i + 1) / len(stock_list), f"Scanning: {symbol}")
            ticker_symbol = symbol + ".NS"
            df_raw = yf.download(ticker_symbol, period=_config['DATA_PERIOD'], interval="1d", auto_adjust=False, progress=False, timeout=10)
            if df_raw.empty: continue
            
            df = clean_data(df_raw)
            if df.empty or len(df) < 100: continue
            
            df = add_all_indicators(df, _config)
            df = apply_trading_logic(df, _config)

            if check_scanner_conditions(df):
                passing_stocks_data[symbol] = df
        except Exception as e:
            logging.error(f"Error scanning {symbol}: {e}")
            continue
    progress_bar.empty()
    return passing_stocks_data

if run_button:
    st.session_state.passing_data = run_full_scan(CONFIG)

# --- DISPLAY RESULTS ---
if 'passing_data' in st.session_state:
    passing_data = st.session_state.passing_data
    
    if not passing_data:
        st.warning("❌ No stocks matched the criteria. Try adjusting the settings or stock list.")
    else:
        st.success(f"✅ Found {len(passing_data)} matching stock(s)!")
        
        # --- Summary Table with Sorting ---
        summary_list = []
        for symbol, df in passing_data.items():
            latest = df.iloc[-1]
            summary_list.append({
                "Symbol": symbol,
                "Close": latest['Close'],
                "Change %": latest['Change %'],
                "Volume": latest['Volume'],
                "RSI": latest['RSI14']
            })
        summary_df = pd.DataFrame(summary_list).set_index("Symbol")
        st.subheader("Screener Results")
        st.dataframe(summary_df.style.format({
            "Close": "₹{:.2f}", "Change %": "{:+.2f}%", "Volume": "{:,.0f}", "RSI": "{:.2f}"
        }).applymap(lambda v: 'color: green' if v > 0 else 'color: red', subset=['Change %']))

        # --- Detailed Analysis Section ---
        st.subheader("Detailed Analysis & Backtest")
        selected_stock = st.selectbox("Select a stock to analyze:", options=list(passing_data.keys()))

        if selected_stock:
            df = passing_data[selected_stock]
            
            # --- TABS FOR CLEAN LAYOUT ---
            tab1, tab2 = st.tabs(["📊 Chart", "📜 Backtest Results"])

            with tab1:
                plot_df = df.tail(CONFIG['PLOT_DAYS'])
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.8, 0.2])
                fig.add_trace(go.Candlestick(x=plot_df.index, open=plot_df['Open'], high=plot_df['High'], low=plot_df['Low'], close=plot_df['Close'], name=selected_stock), row=1, col=1)
                fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df[f'EMA{CONFIG["EMA_SHORT"]}'], mode='lines', name=f'EMA {CONFIG["EMA_SHORT"]}', line=dict(color='green')), row=1, col=1)
                fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df[f'EMA{CONFIG["EMA_MEDIUM"]}'], mode='lines', name=f'EMA {CONFIG["EMA_MEDIUM"]}', line=dict(color='red')), row=1, col=1)
                fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['ATR_Stop'], mode='lines', name='ATR Stop-Loss', line=dict(color='orange', width=2, dash='dot')), row=1, col=1)
                fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['Buy_Marker'], mode='markers', name='Buy Signal', marker=dict(color='lime', size=12, symbol='triangle-up', line=dict(width=1, color='black'))), row=1, col=1)
                
                vol_colors = ['green' if r['Close'] >= r['Open'] else 'red' for _, r in plot_df.iterrows()]
                fig.add_trace(go.Bar(x=plot_df.index, y=plot_df['Volume'], name='Volume', marker_color=vol_colors), row=2, col=1)
                
                fig.update_layout(height=700, template='plotly_dark', showlegend=True, margin=dict(l=20, r=20, t=40, b=20), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.write(f"Running backtest for **{selected_stock}** over the last **{CONFIG['DATA_PERIOD']}**...")
                summary, trades_df = run_backtest_with_atr_stop(df, CONFIG['BACKTEST_CAPITAL'])
                if isinstance(summary, dict):
                    st.metric("Final PnL", value=summary['Total PnL'])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Win Rate", value=summary['Win Rate'])
                    col2.metric("Total Trades", value=summary['Total Trades'])
                    col3.metric("Final Capital", value=summary['Final Capital'])
                    
                    st.write("---")
                    st.write("All Trades:")
                    st.dataframe(trades_df.style.format({
                        "EntryPrice": "₹{:.2f}", "ExitPrice": "₹{:.2f}", "PnL": "₹{:,.2f}"
                    }), use_container_width=True)
                else:
                    st.info(summary)
