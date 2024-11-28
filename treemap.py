import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
merged_df = pd.read_csv('data/merged_sp500_data.csv')

app.layout = html.Div([
    html.H4("Interactive TreeMap with Dash"),
    dcc.Dropdown(
        id='filter-options',
        value='shareholder_company',
        options=[
            # Holder -> Sector -> Industry -> Company
            {'label': 'Holder > Sector > Industry > Company', 'value': 'shareholder_sector'},
            # Holder -> Company
            {'label': 'Holder > Company', 'value': 'shareholder_company'},
            # Sector -> Holder 
            {'label': 'Sector > Holder', 'value': 'sector'},
            # Company -> Holder
            {'label': 'Company > Holder', 'value': 'company'},
        ],
        clearable=False
    ),
    dcc.Graph(id="graph", style={'height': '800px'}),
])

@app.callback(
    Output("graph", "figure"),
    Input("filter-options", "value"))

def generate_chart(mode):
    if mode == 'shareholder_sector':
        # Path: sp500 -> Holder -> Sector -> Industry -> Company
        fig = px.treemap(
            merged_df,
            path=[px.Constant("sp500"), 'name', 'sector', 'industry', 'symbol'],
            values='value',
            color='value',
            color_discrete_map={"sp500": "lightgray"},
            color_continuous_scale='RdBu',
            maxdepth=3
        )
    elif mode == 'shareholder_company':
        # Path: sp500 -> Holder -> Company
        fig = px.treemap(
            merged_df,
            path=[px.Constant("sp500"), 'name', 'symbol'],
            values='value',
            color='value',
            color_discrete_map={"sp500": "lightgray"},
            color_continuous_scale='RdBu',
            maxdepth=3
        )
    elif mode == 'sector':
        # Path: sp500 -> Sector -> Holder
        fig = px.treemap(
            merged_df,
            path=[px.Constant("sp500"), 'sector', 'name'],
            values='value',
            color='value',
            color_discrete_map={"sp500": "lightgray"},
            color_continuous_scale='RdBu',
        )
    else:
        # Path: sp500 -> Company -> Holder
        fig = px.treemap(
            merged_df,
            path=[px.Constant("sp500"), 'symbol', 'name'],
            values='value',
            color='value',
            color_discrete_map={"sp500": "lightgray"},
            color_continuous_scale='RdBu',
        )

    fig.update_traces(
        marker_line_width = 0,
        hovertemplate=(
            '<b>%{label}</b><br>' +
            'Path: %{id}<br>' +
            'Value: %{value:,.2f}$<extra></extra>'
        ),
        hoverlabel=dict(
            bgcolor="lightgray",  # Set background color
            font_size=14,         # Customize font size
            font_color="black",   # Set font color
            bordercolor="black"    # Set border color
        ),
    )
    
    fig.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        paper_bgcolor="lightgray",    # Set the entire figure background color
        plot_bgcolor="lightgray"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)