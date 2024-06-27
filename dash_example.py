from dash import Dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

from sklearn.datasets import load_iris


app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.BOOTSTRAP])

df = pd.read_csv('./Results.csv')


def transparent_button_with_icon(button_id, icon, text):

    button = html.Button([
        html.Div(className=icon, style={"margin":"10px"}),
        text
        ],
        style={
            "background-color":"transparent",
            "border":"none",
        },
        id=button_id,
        n_clicks=0
    )
    return button


navbar = dbc.Navbar([
    html.Button(
        html.Div(className="bi bi-list me-5"),
        style={
            "background-color":"transparent",
            "border":"none",
            'font-size': '30px',
            'color': 'white'
        },
    ),
    dbc.NavItem(dbc.NavLink("Home", href="/")),
],
    color="primary",
    dark=True,
)


content = dbc.Row(
    [
        dbc.Col([
            dbc.Card(
                [dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])]
            )], width=12
        ),
    ],
)

app.layout = dbc.Container(
    [navbar, content], fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
