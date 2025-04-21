import sys
import pandas as pd
import plotly.graph_objects as go
from binance.client import Client

# 1. SETUP PATHS AND IMPORTS
sys.path.append(r'D:/plotlyfinance')
try:
    import plotlyfinance as pf
except ImportError as e:
    print(f"Import Error: {e}\nCheck your package structure!")
    raise

# 2. BINANCE DATA FETCHER (WITH COLUMN NAME FIX)
def get_binance_data(symbol='BTCUSDT', interval='1d', lookback='100 days ago UTC'):
    """Returns DataFrame with consistent column names"""
    try:
        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=lookback
        )
        columns = [
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades',
            'tb_base_vol', 'tb_quote_vol', 'ignore'
        ]
        df = pd.DataFrame(klines, columns=columns)
        
        # Convert and standardize
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.set_index('date')
        return df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise

# 3. INITIALIZE BINANCE CLIENT
try:
    client = Client()  # Note: You may need to provide API key and secret
except Exception as e:
    print(f"Binance client initialization error: {e}")
    raise

# 4. FETCH AND PREPARE DATA
try:
    btc_data = get_binance_data(interval='1d', lookback='30 days ago UTC')
    print("Data sample:\n", btc_data.head())
    
    # Add indicators (using lowercase columns)
    btc_data['sma_20'] = btc_data['close'].rolling(window=20).mean()
    btc_data['sma_50'] = btc_data['close'].rolling(window=50).mean()
    
except Exception as e:
    print(f"Data processing error: {e}")
    raise

# 5. PLOT WITH ERROR HANDLING
try:
    fig = go.Figure()
    
    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=btc_data.index,
        open=btc_data['open'],
        high=btc_data['high'],
        low=btc_data['low'],
        close=btc_data['close'],
        name='BTC/USDT'
    ))
    
    # SMAs
    fig.add_trace(go.Scatter(
        x=btc_data.index,
        y=btc_data['sma_20'],
        name='SMA 20',
        line=dict(color='orange', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=btc_data.index,
        y=btc_data['sma_50'],
        name='SMA 50',
        line=dict(color='purple', width=2)
    ))
    
    # Layout
    fig.update_layout(
        title='BTC/USDT with Moving Averages',
        yaxis_title='Price (USDT)',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )
    
    fig.show()
    
except Exception as e:
    print(f"Plotting error: {e}")
    raise