import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
merged_df = pd.read_csv('data/merged_sp500_data.csv')

app.layout = html.Div([
    html.H4("Interactive TreeMap with Dash"),
    html.P("Values grouped by:"),
        dcc.Dropdown(
        id='filter-options',
        value='shareholder',
        options=[
            {'label': 'Shareholders by Company', 'value': 'shareholder'},
            {'label': 'Sector', 'value': 'sector'},
            {'label': 'Industry', 'value': 'industry'},
            {'label': 'Country', 'value': 'country'}
        ],
        clearable=False
    ),
    dcc.Graph(id="graph", style={'height': '800px'}),
])

@app.callback(
    Output("graph", "figure"),
    Input("filter-options", "value"))

def generate_chart(mode):
    if mode == 'shareholder':
        merged_df["filter"] = merged_df["name"]  
    elif mode == 'sector':
        merged_df["filter"] = merged_df["sector"]
    elif mode == 'industry':
        merged_df["filter"] = merged_df["industry"]
    elif mode == 'country':
        merged_df["filter"] = merged_df["country"]

    fig = px.treemap(
        merged_df,
        path=[px.Constant("sp500"), 'filter', 'symbol'],
        values='value',
        color='value',
        hover_data=['shares'],
        color_continuous_scale='RdYlGn',    
    )
    

    fig.update_traces(root_color="white")
    fig.update_traces(marker_line_width = 0)
    fig.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        paper_bgcolor="lightgray",    # Set the entire figure background color
        plot_bgcolor="lightgray")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)