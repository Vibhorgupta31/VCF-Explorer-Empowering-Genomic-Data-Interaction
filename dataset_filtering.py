from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf
from dash_app import app

layout = html.Div([
            html.H1("Enter region to filter (format should be chr:start:end or chr, comma seperated)", style={'textAlign': 'center'}),
            dbc.Row(
                [
                    dbc.Col('Path to tiledb dataset', width= 6),
                    dcc.Input(placeholder="20:1-50000", id= "filter_region", type='text'),
                    html.Button('Submit', id='submit-val', n_clicks=0)
                ]
            ),
    dash_table.DataTable(id="table")
#             html.Div(id="filtered_datset")
        ])

# @app.callback(Output("filtered_datset", "children"), [Input("filter_region", "value")])

@callback(
    Output('table', 'data'),
    Input('submit-val', 'n_clicks'),
    State('filter_region', 'value'),
    prevent_initial_call=True
)
def filter_dataset(n_clicks, regions):
    dataset_path = pathlib.Path( "./Data")
    regionList = regions.split(",")
    ds = tiledbvcf.Dataset(str(dataset_path),"r")
#     df = ds.read(regions = regionList)
    df = ds.read(regions = ["20:14370-1110696"], attrs = ["sample_name", "pos_start"])
    return df.to_dict('records')
# return dash_table.DataTable(df.to_dict('records'))