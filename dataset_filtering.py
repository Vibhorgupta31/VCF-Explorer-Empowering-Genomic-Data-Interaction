from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf
from dash_app import app

dataset_path = pathlib.Path( "./Data")

ds = tiledbvcf.Dataset(str(dataset_path),"r")

layout = html.Div([
            html.H1("Enter region to filter (format should be chr:start:end or chr, comma seperated)", style={'textAlign': 'center'}),
            dcc.Input(placeholder="20:1-50000", id= "filter_region", type='text'),
            dcc.Dropdown(id='sample-filter', options=list(ds.samples()), multi=True),
            html.Button('Submit', id='submit-val', n_clicks=0),
            dash_table.DataTable(id="table")
        ])

# @app.callback(Output("filtered_datset", "children"), [Input("filter_region", "value")])

@callback(
    Output('table', 'data'),
    Input('submit-val', 'n_clicks'),
    State('filter_region', 'value'),
    State('sample-filter', 'value'),
    prevent_initial_call=True
)
def filter_dataset(n_clicks, regions, samples):
    regionList = regions.split(",")
    regionList = [x.strip() for x in regionList]
    df = ds.read(regions = regionList, samples=samples, attrs = ["sample_name", "pos_start"])
    return df.to_dict('records')