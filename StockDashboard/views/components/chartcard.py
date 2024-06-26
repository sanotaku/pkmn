from datetime import date
from datetime import timedelta

from dash import dcc
from dash import html
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from api.network import get_stock
from api.network import get_stock_summary


def chart_card_factory(stock_code: str, periods: int) -> dbc.Card:
    df = get_stock(stock_code)

    df = df.tail(periods)

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
        title='CLE vs Model',
        yaxis2=dict(
            overlaying='y',
            side='right'
        )
    )

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.2, 0.2, 0.2]
    )


    fig.append_trace(
        go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close, increasing_line_color= 'red', decreasing_line_color= 'green', name='株価', yaxis='y1'),
        row=1, col=1)
    fig.append_trace(
        go.Scatter(x=df.index, y=df.MA5, line=dict(color='blue', width=1), name='MA-5', yaxis='y1'),
        row=1, col=1)
    fig.append_trace(
        go.Scatter(x=df.index, y=df.MA25, line=dict(color='red', width=1), name='MA-25', yaxis='y1'),
        row=1, col=1)
    fig.append_trace(
        go.Scatter(x=df.index, y=df.MA75, line=dict(color='green', width=1), name='MA-75', yaxis='y1'),
        row=1, col=1)
    fig.append_trace(
        go.Scatter(x=df.index, y=df.MA200, line=dict(color='purple', width=1), name='MA-200', yaxis='y1'),
        row=1, col=1)
    
    fig.append_trace(
        go.Bar(x=df.index, y=df.Volume, name='Volume', yaxis='y1'),
        row=2, col=1)
    

    fig.append_trace(
        go.Scatter(x=df.index, y=df.RSI, line=dict(color='green', width=1), name='RSI', yaxis='y1'),
        row=3, col=1)
    
    fig.append_trace(
        go.Scatter(x=df.index, y=df.MACD, line=dict(color='blue', width=1), name='MAXD', yaxis='y1'),
        row=4, col=1)
    fig.append_trace(
        go.Scatter(x=df.index, y=df.SIGNAL, line=dict(color='red', width=1), name='SIGNAL', yaxis='y1'),
        row=4, col=1)
    # fig = go.Figure(data=[
    #         go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close, increasing_line_color= 'red', decreasing_line_color= 'green', name='株価', yaxis='y1'), 
    #         go.Scatter(x=df.index, y=df.MA5, line=dict(color='blue', width=1), name='MA-5', yaxis='y1'),
    #         go.Scatter(x=df.index, y=df.MA25, line=dict(color='red', width=1), name='MA-25', yaxis='y1'),
    #         go.Scatter(x=df.index, y=df.MA75, line=dict(color='green', width=1), name='MA-75', yaxis='y1'),
    #         go.Scatter(x=df.index, y=df.MA200, line=dict(color='purple', width=1), name='MA-200', yaxis='y1'),
    #         go.Bar(x=df.index, y=df['Volume'], yaxis='y2', opacity=0.5)
    #     ], layout=layout)

    fig.update_xaxes(rangebreaks=[dict(values=missing)])
    fig.update_layout(
        autosize=True,
        # width=500,
        height=500,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        showlegend=False
    )
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        xaxis3_rangeslider_visible=False,
        xaxis4_rangeslider_visible=True,
        xaxis4_rangeslider_thickness=0.1,
        xaxis_type="date"
    )

    yestaday_rate = round((df.Close.tail(2).values[1] - df.Close.tail(2).values[0]) / df.Close.tail(2).values[0] * 100, 2)

    yestaday_rate_label = None
    if yestaday_rate >= 0:
        yestaday_rate_label = html.H5(f'+{yestaday_rate}%', style={'color':'red'})
    else:
        yestaday_rate_label = html.H5(f'{yestaday_rate}%', style={'color':'green'})


    stock_sumary = get_stock_summary(stock_code)

    return dbc.Card([
        dbc.CardBody([
            dbc.Container([
                dbc.Row([html.H5(f'{stock_code} {stock_sumary["company_name"]}')]),
                dbc.Row([html.P(f'PER: {stock_sumary["per"]} / PBR: {stock_sumary["pbr"]} 時価総額: {stock_sumary["capital"]}億円'), html.P(yestaday_rate_label)]),
                dbc.Row(dcc.Graph(figure=fig)),
            ], fluid=True)
        ])
    ])