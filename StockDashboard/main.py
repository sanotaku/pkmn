import warnings

from dash import Dash
from dash import page_container
import dash_bootstrap_components as dbc


warnings.simplefilter('ignore')

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], use_pages=True, pages_folder='views')


navbar = dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink("Home", href="/")),
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Home",  href="/", header=True),
            dbc.DropdownMenuItem("ウォッチリスト", href="/WatchList"),
            dbc.DropdownMenuItem("52週高値", href="/HighPrice"),
            dbc.DropdownMenuItem("アラート", href="/Alert"),
        ],
        nav=True,
        in_navbar=True,
        label="More",
    ),
],
    brand="Stock Analysis System",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = dbc.Container([
    navbar,
    dbc.Row(dbc.Col(page_container, width=12))
], fluid=True)

app.run(host='0.0.0.0', port=8080, debug=False)
