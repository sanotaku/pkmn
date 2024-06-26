from datetime import date
from datetime import timedelta

from dash import register_page
from dash import dcc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from views.components.kpi_card import kpi_card_factory
from views.components.stock_chart_fig import stock_chart_fig_factory
from api.network import get_stock_by_stooq


register_page(__name__, path='/')


def nikkei_rev_fig(_df: pd.DataFrame):
    df = _df

    df = df.tail(120)

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

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.2, 0.2]
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


    fig.update_xaxes(rangebreaks=[dict(values=missing)])
    fig.update_layout(
        autosize=True,
        height=400,
        margin = dict(l=40, r=40, t=20, b=40, autoexpand=False),
        showlegend=False
    )
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        xaxis2_rangeslider_visible=False,
        xaxis3_rangeslider_visible=False,
        xaxis_type="date"
    )

    return fig

df_nikkei_rev = get_stock_by_stooq('1570').tail(120)
df_nikkei = get_stock_by_stooq(f'^NKX', is_js_suffix=False).tail(160)
df_topix = get_stock_by_stooq(f'^TPX', is_js_suffix=False).tail(160)

previous_rsi = round(df_nikkei_rev.RSI.tail(1).values[0], 2)
yestaday_rate = round((df_nikkei_rev.Close.tail(2).values[1] - df_nikkei_rev.Close.tail(2).values[0]) / df_nikkei_rev.Close.tail(2).values[0] * 100, 2)




nikkei_rev_card = dbc.Card([
    dbc.Container([
        dbc.Row([
            html.H5('Nikkei レバレッジETF'),
            dbc.Col(dbc.Card(dbc.Row(dcc.Graph(figure=nikkei_rev_fig(df_nikkei_rev)))), width=9),
            dbc.Col(
                dbc.Card(
                    dbc.Container([
                        dbc.Row(dbc.Col(kpi_card_factory('RSI', previous_rsi), class_name='m-2')),
                        dbc.Row(dbc.Col(kpi_card_factory('前日比', f'{yestaday_rate}%'), class_name='m-2')),
                    ])
                ), width=3
            )
        ])
    ], class_name='m-1', fluid=True)
], class_name='m-2')


nikkei_225_card = dbc.Card(
    dbc.Container(dbc.Row([
        html.H5('Nikkei-225'),
        dcc.Graph(figure=stock_chart_fig_factory(df_nikkei))
    ])), class_name='m-2'
)

topix_card = dbc.Card(
    dbc.Container(dbc.Row(dbc.Col([
        html.H5('TOPIX'),
        dcc.Graph(figure=stock_chart_fig_factory(df_topix))
    ]))), class_name='m-2'
)

nt_rate_card = dbc.Card(
    dbc.Container(dbc.Row(dbc.Col([
        html.H5('NT倍率'),
        dcc.Graph(figure=go.Figure(
            go.Scatter(x=df_nikkei.index, y=df_nikkei.Close / df_topix.Close),
            layout = go.Layout(
                height=300,
                margin = dict(l=40, r=40, t=20, b=40, autoexpand=False),
                showlegend=False,
            )
        ))
    ]))), class_name='m-2'
)

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(nikkei_rev_card, width=6),
        ]),
        dbc.Row([
            dbc.Col(nikkei_225_card, width=6),
            dbc.Col(topix_card, width=6),
        ]),
        dbc.Row([
            dbc.Col(nt_rate_card, width=6),
        ])
    ], fluid=True),
], className='my-2')
