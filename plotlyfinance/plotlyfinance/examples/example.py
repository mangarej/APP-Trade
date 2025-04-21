import sys
import os

# Add the plotlyfinance directory to the Python path
sys.path.append(r'D:/plotlyfinance')

import pandas as pd
import numpy as np
import plotlyfinance as pf
import plotly.io as pio

# Set renderer BEFORE fig.show()
pio.renderers.default = "vscode"

# Create sample data
data = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=100),
    'Open': np.random.rand(100) * 100,
    'High': np.random.rand(100) * 110,
    'Low': np.random.rand(100) * 90,
    'Close': np.random.rand(100) * 100,
    'Volume': np.random.randint(1000, 10000, 100)
}).set_index('Date')

# Plot candlestick with volume and SMA
fig = pf.plot(data, type='candle', title='Sample Stock Chart', style='yahoo', volume=True, add_indicators=['sma'])
fig.show()
