from datetime import date
from datetime import timedelta

from dash import Input
from dash import Output
from dash import callback
from dash import register_page
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from api.database import get_high_price_log


register_page(__name__, path='/HighPrice')


@callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '

    start_date_object = None
    end_date_object = None

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        df_all = get_high_price_log(start_date_object, end_date_object)
        df_etl = get_high_price_log(start_date_object, end_date_object)
        df_etl = df_etl[df_etl['count'] == 1]

        return dbc.Card(
            dbc.Row([
                dbc.Col(dbc.Card(dbc.Table.from_dataframe(df_all)), width=6),
                dbc.Col(dbc.Card(dbc.Table.from_dataframe(df_etl)), width=6),
            ])
        )
        

df_all = get_high_price_log(date.today() - timedelta(7), date.today())
df_etl = get_high_price_log(date.today() - timedelta(7), date.today())
df_etl = df_etl[df_etl['count'] == 1]

card = dbc.Card(
    dbc.Row([
        dbc.Col(dbc.Card(dbc.Table.from_dataframe(df_all)), width=6),
        dbc.Col(dbc.Card(dbc.Table.from_dataframe(df_etl)), width=6),
    ])
)


layout = [
    dbc.Card([
        dbc.CardHeader('検索範囲', class_name='my-1'),
        dbc.CardBody([
            dcc.DatePickerRange(id='my-date-picker-range', start_date=date.today() - timedelta(7), end_date=date.today()),
            html.Div(id='output-container-date-picker-range', children=card)
        ], class_name='my-1')
    ], class_name='my-1')
]
