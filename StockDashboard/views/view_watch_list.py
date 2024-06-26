from dash import register_page
from dash import html
import dash_bootstrap_components as dbc

from views.components.chartcard import chart_card_factory
from api.database import get_watch_list_code

register_page(__name__, path='/WatchList')


dbc_rows = []
CHART_COLUMN_NUM = 3

watch_list = get_watch_list_code()
split_watch_list = []

for i in range(0, len(watch_list), CHART_COLUMN_NUM):
    split_watch_list.append(watch_list[i: i + CHART_COLUMN_NUM])

for stock_codes in split_watch_list:
    dbc_cols = []
    for stock_code in stock_codes:
        dbc_cols.append(dbc.Col(chart_card_factory(stock_code, 90), class_name='my-1', width=12/CHART_COLUMN_NUM))
    dbc_rows.append(dbc.Row(dbc_cols))

layout = html.Div([
    dbc.Container(dbc_rows, class_name='m-1', fluid=True)
])
