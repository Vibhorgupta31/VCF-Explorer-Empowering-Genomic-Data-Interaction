from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf

# from dashApp import app

layout = html.Div([
            html.H1("Select tiledb dataset and add vcf files (if required)", style={'textAlign': 'center'}),
            dbc.Row(
                [
                    dbc.Col('Path to tiledb dataset', width= 6),
                    dcc.Input(placeholder="Enter the path of the tiledb dataset to be created or default tiledbtest will be used", id= "dataset_path", type='text')
                ]
            ),
            dbc.Row(
                [
                    dbc.Col('Path to vcf file directory', width= 6),
                    dcc.Input(placeholder="Enter the path of the directory containing vcfs", id= "vcf_path", type='text')
                ]
            ),
            html.Div(id="dataset_creation_report")
        ])


# @app.callback(Output("dataset_creation_report", "children"), [Input("vcf_path", "value")])
# def render_page_content(vcf_path):
#    return vcf_path