import dash
from dash import html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Alternate text positions to reduce overlap
text_positions = ["top left", "top center", "top right", "middle left", "middle center", "middle right", "bottom left", "bottom center", "bottom right"]

# Load service account credentials from environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS")
creds_dict = json.loads(creds_json)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Authorize with gspread
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# Open the spreadsheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1zMobZwRyBjmCPBR8G37y08Bs5YCLWvbTVg3VWLQ57o8")
sheet = spreadsheet.worksheet("df")

# Get data into pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)

selected_columns = ['Project', 'Type', 'Milestone', 'Date', 'RAG']
df = df[selected_columns]

colour_map = {"Red": "red", "Amber": "orange", "Green": "green"}
fig = px.scatter(df, y = "Project", x = "Date", color = "RAG", hover_data = ["Milestone", "Date"], color_discrete_map=colour_map)

dash.register_page(__name__, path='/') # path='/' makes this the homepage

layout = html.Div([html.Br(), html.H5("Filters"),
                   html.Div([dbc.Row([dbc.Col(html.Div(dcc.Dropdown(id="Project-Filter", options=[{"label": col, "value": col} for col in df["Project"].unique()],value=None, placeholder="Filter by Project", clearable=True
                                                                    )),width=6)])]),
                   html.Br(),
                   dcc.Graph(id="scatter-graph",figure=fig, style={'width': '100%', 'height': '85vh'})])

# Callback for Filtering

@dash.callback(
    Output("scatter-graph", "figure"),
    Input("Project-Filter", "value")
)

def update_graph(selected_project):
    filtered_df = df if selected_project is None else df[df["Project"] == selected_project]

    fig = px.scatter(filtered_df,y = "Project", x = "Date", color = "RAG", hover_data = ["Milestone", "Date"], color_discrete_map=colour_map)

    if selected_project and len(filtered_df["Project"].unique()) == 1:
        for i, row in filtered_df.iterrows():
            fig.add_annotation(
                x=row["Date"],
                y=row["Project"],
                text=row["Milestone"],
                font=dict(size=12, color="black"),
            )



    return fig