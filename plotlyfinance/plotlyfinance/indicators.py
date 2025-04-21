# plotlyfinance/indicators.py
import pandas as pd

def add_sma(data, window=20, column='Close'):
    """Calculate and return Simple Moving Average."""
    return data[column].rolling(window=window).mean()

def add_rsi(data, window=14, column='Close'):
    """Calculate and return Relative Strength Index."""
    delta = data[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_bollinger_bands(data, window=20, num_std=2):
    """Add Bollinger Bands"""
    sma = data['Close'].rolling(window).mean()
    std = data['Close'].rolling(window).std()
    
    data[f'BB_upper_{window}'] = sma + (std * num_std)
    data[f'BB_lower_{window}'] = sma - (std * num_std)
    return data

def add_macd(data, fast=12, slow=26, signal=9):
    """Add MACD"""
    exp1 = data['Close'].ewm(span=fast).mean()
    exp2 = data['Close'].ewm(span=slow).mean()
    
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=signal).mean()
    return data
