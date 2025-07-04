
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

#start of dash app
external_stylesheets = [dbc.themes.LUX]

app = Dash(__name__, use_pages=True,external_stylesheets=external_stylesheets)
server = app.server

dropdown = dbc.DropdownMenu(
    label="More Pages",
    children=[
        dbc.DropdownMenuItem(page["name"], href=page["relative_path"])
        for page in dash.page_registry.values()
    ],
    nav=True, in_navbar=True
)

navbar = dbc.NavbarSimple(
    children=[dropdown],
    brand="Plan on a Page",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)

print(dash.page_registry.values())