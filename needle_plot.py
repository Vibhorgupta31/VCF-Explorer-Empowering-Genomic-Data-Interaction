from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf
from dash_app import app
import dash_bio as dashbio
import re
from dash.exceptions import PreventUpdate

layout = html.Div([
            html.H1("Enter region to plot (format should be chr:start,end)", style={'textAlign': 'center'}),
            dbc.Row(
                [
                    dcc.Input(placeholder="20:1-50000", id= "filter_region", type='text'),
                    html.Button('Submit', id='submit-val', n_clicks=0)
                ]
            ),
#             html.Div(id="placeholder"),
            dashbio.NeedlePlot(
                id='dashbio-default-needleplot')
        ])

# @app.callback(Output("filtered_datset", "children"), [Input("filter_region", "value")])

@callback(
    Output('dashbio-default-needleplot', 'mutationData'),
#     Output('placeholder', 'children'),
    Input('submit-val', 'n_clicks'),
    State('filter_region', 'value'),
    prevent_initial_call=True
)
def plot_dataset(n_clicks, regions):
#     return n_clicks
# #     if n_clicks<=1:
# #         raise PreventUpdate
    dataset_path = pathlib.Path( "./Data")
    regionList = regions.strip()
    match = re.search(r"(?<=:)\d+", regionList)
    start_location = int(match.group()) if match else 0
    ds = tiledbvcf.Dataset(str(dataset_path),"r")
#     df = ds.read(regions = regionList)
#     df = ds.read(regions = ["20:14370-1110696"])
    df = ds.read(regions = regionList)
    groupedDf = df.groupby(['contig','pos_start']).agg({'sample_name' : 'count'}).reset_index()
    groupedDf['rel_pos'] = groupedDf['pos_start'] - start_location
    mdata = {}
    mdata['x'] = [str(x) for x in list(groupedDf['rel_pos'])]
    mdata['y'] = [str(x) for x in list(groupedDf['sample_name'])]
    return mdata