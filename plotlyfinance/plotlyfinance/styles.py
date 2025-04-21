# plotlyfinance/styles.py
def apply_style(fig, style):
    """Apply predefined styles to the chart."""
    if style == 'yahoo':
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_gridcolor='lightgray',
            yaxis_gridcolor='lightgray'
        )
    elif style == 'night':
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='black',
            paper_bgcolor='black',
            xaxis_gridcolor='gray',
            yaxis_gridcolor='gray'
        )
    else:
        fig.update_layout(template='plotly')