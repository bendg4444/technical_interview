
import dash
from dash import Dash, dcc, html, Output, Input, callback
import dash_daq as daq
import dash_bootstrap_components as dbc
from app import data
departments = [
    'All',
    'Drawings & Prints',
    'Photography',
    'Painting & Sculpture',
    'Media and Performance',
    'Architecture & Design'
]

dash.register_page(__name__, path="/")

layout = \
    html.Div([
        # Header Bar
        html.Div([
            html.H1(children="Museum of Modern Art: Data Analysis")
        ]),

        html.Hr(),

        # Input values
        html.Div([
    
            html.Div([
                html.H2("Department:")
            ], style={"width": "30%", "display": "inline-block"}),

            html.Div([
                dcc.Dropdown(departments, value="All",
                             id="department-dropdown")
            ], style={"display": "inline-block", "width": "46%"}),

        ]),

        html.Div([

            html.Div([
                html.H2("Finished Between Years:")
            ], style={"width": "30%", "display": "inline-block"}),

            html.Div([
                daq.NumericInput(
                    id="year-start",
                    min=data['year_completed'].min(),
                    max=data['year_completed'].max(),
                    value=data['year_completed'].min(),
                    size=300,

                )
            ], style={"display": "inline-block", "width": "25%"}),

            html.Div([
    
                daq.NumericInput(
                    id="year-end",
                    min=data['year_completed'].min(),
                    max=data['year_completed'].max(),
                    value=data['year_completed'].max(),
                    size=300
                )
            ], style={"display": "inline-block", "width": "33%"}),

            html.Div([
                html.P(id='error-warning', style={"color": "red"})
            ], style={"display": "inline-block", "width": "33%"}),
            
        ], style={"padding-top": "3px"}),

        html.Hr(),

        # Number of artworks
        html.Div([
            html.H3(id="num-of-artworks")
        ], style={'padding-top': '5px'}),

        html.Hr(),

        # Graphs
        html.Div([

            html.Div([
                dcc.Graph(id="gender-graph")
            ], style={"display": "inline-block", "width": "50%"}),

            html.Div([
                dcc.Graph(id="nationality-graph")
            ], style={"display": "inline-block", "width": "50%"}),

        ]),

        html.Hr(),

        #  Descriptive String
        html.Div([
            html.Div(html.H3(id="descriptive-string"))
        ], style={'align': 'center'}),

        html.Hr(),


    ], style={"padding": "12px"})
