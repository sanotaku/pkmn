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


register_page(__name__, path='/Alert')



def layout():
    return html.H5('test...')

