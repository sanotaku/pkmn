from datetime import date
from datetime import timedelta

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def stock_chart_fig_factory(_df: pd.DataFrame) -> go.Figure:
    df = _df

    ds = []

    for datetime_index in df.index:
        ds.append(date(
            int(str(datetime_index).split(' ')[0].split('-')[0]),
            int(str(datetime_index).split(' ')[0].split('-')[1]),
            int(str(datetime_index).split(' ')[0].split('-')[2])
        ))

    df['Date'] =  ds
    alldays = set(
        df.Date[0] + timedelta(x) for x in range((df.Date[len(df.Date)-1]- df.Date[0]).days)
    )
    missing = sorted(set(alldays)-set(df.Date))

    layout = go.Layout(
        height=300,
        yaxis2=dict(
            overlaying='y',
            side='right'
        ),
        margin = dict(l=40, r=40, t=20, b=40, autoexpand=False),
        showlegend=False,
    )

    fig = go.Figure(data=[
        go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close, increasing_line_color= 'red', decreasing_line_color= 'green', name='株価', yaxis='y1'), 
        go.Scatter(x=df.index, y=df.MA5, line=dict(color='blue', width=1), name='MA-5', yaxis='y1'),
        go.Scatter(x=df.index, y=df.MA25, line=dict(color='red', width=1), name='MA-25', yaxis='y1'),
        go.Scatter(x=df.index, y=df.MA75, line=dict(color='green', width=1), name='MA-75', yaxis='y1'),
        go.Scatter(x=df.index, y=df.MA200, line=dict(color='purple', width=1), name='MA-200', yaxis='y1'),
        go.Bar(x=df.index, y=df.Volume, yaxis='y2', opacity=0.5)
    ], layout=layout)


    fig.update_layout(layout)
    fig.update_layout(
        xaxis_rangeslider_visible=False
    )
    fig.update_xaxes(rangebreaks=[dict(values=missing)])


    return fig
