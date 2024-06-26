# <div id="container">
#   <div class="kpi-card orange">
#     <span class="card-value">$ 1,342 </span>
    
#     <span class="card-text">Total Sales</span>
#      <i class="fas fa-shopping-cart icon"></i>
#   </div>
 
 
#     <div class="kpi-card purple">
#     <span class="card-value">$ 1,342 </span>
#     <span class="card-text">Total Sales</span>
#        <i class="fas fa-shopping-cart icon"></i>
#   </div>
  
#       <div class="kpi-card grey-dark">
#     <span class="card-value">$ 1,342 </span>
#     <span class="card-text">Total Sales</span>
#          <i class="fas fa-shopping-cart icon"></i>
#   </div>
  
#     <div class="kpi-card red">
#     <span class="card-value">$ 1,342 </span>
#     <span class="card-text">Total Sales</span>
#       <i class="fas fa-shopping-cart icon"></i>
#   </div>
# </div>

import dash_bootstrap_components as dbc
from dash import html


def kpi_card_factory(title: str, body: str, color: str='primary'):
    kpi_card = dbc.Card([
        dbc.Container([
            dbc.Row(dbc.Col(html.H6(title))),
            dbc.Row(dbc.Col(html.P(body)))
        ])
    ], color=color)

    return kpi_card
