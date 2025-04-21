# plotlyfinance/plot.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from .styles import apply_style
from .utils import validate_data

def plot(data, type='candle', title='Financial Chart', style='default', volume=False, add_indicators=None):
    """
    Plot financial data using Plotly.
    
    Parameters:
    - data: pandas DataFrame with columns ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    - type: 'candle' or 'ohlc'
    - title: Chart title
    - style: Style/theme (e.g., 'yahoo', 'night')
    - volume: Boolean to include volume subplot
    - add_indicators: List of indicators (e.g., ['sma', 'rsi'])
    """
    # Validate DataFrame
    validate_data(data, required_cols=['Open', 'High', 'Low', 'Close'])

    # Initialize figure with subplots
    rows = 1 + (1 if volume else 0) + (len(add_indicators) if add_indicators else 0)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, subplot_titles=[title])

    # Add candlestick or OHLC
    if type == 'candle':
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ), row=1, col=1
        )
    elif type == 'ohlc':
        fig.add_trace(
            go.Ohlc(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='OHLC'
            ), row=1, col=1
        )

    # Add volume subplot if requested
    if volume and 'Volume' in data.columns:
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color='blue'
            ), row=2, col=1
        )

    # Add indicators if specified
    current_row = 1 + (1 if volume else 0)
    if add_indicators:
        from .indicators import add_sma, add_rsi
        for indicator in add_indicators:
            if indicator == 'sma':
                sma = add_sma(data)
                fig.add_trace(
                    go.Scatter(x=data.index, y=sma, name='SMA', line=dict(color='orange')),
                    row=1, col=1
                )
            elif indicator == 'rsi':
                rsi = add_rsi(data)
                fig.add_trace(
                    go.Scatter(x=data.index, y=rsi, name='RSI', line=dict(color='purple')),
                    row=current_row + 1, col=1
                )
                current_row += 1

    # Apply style
    apply_style(fig, style)

    # Update layout
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        showlegend=True,
        height=600 * rows // 2
    )

    return fig