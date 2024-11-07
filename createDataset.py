# Library Imports
from dash import Dash,html,dcc, Input, Output, State,callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pathlib
import tiledbvcf
from flask import g
import shutil



create_dataset =  html.Div([
    dbc.Label("Directory to VCF Files: "),
    dcc.Input(id = "files_directory", placeholder="Directory to VCF files"),
    html.Br(),
    dbc.Label("Dataset Name: "),
    dcc.Input(id = "dataset", placeholder="Dataset Name ( Default : vcf_dataset )"),
    html.Button('Submit', id='constants_update_submit', n_clicks=0),
    dcc.Loading(
        id="loading-1",
        type="default",
        children=html.Div(id="creation_status")
    )
])


@callback(Output("creation_status", component_property="children"),
          Input("constants_update_submit", component_property="n_clicks"),
          State("dataset", component_property="value"),
          State("files_directory", component_property="value"))
def creation(n_clicks, dataset, files_directory):
    if n_clicks == 0:
        raise PreventUpdate
    FILES_DIRECTORY = pathlib.Path(files_directory)
    if FILES_DIRECTORY.exists()!=True:
        return (dbc.Alert("File path doesn't exits", color="warning"))
    if str(dataset)=='':
        DATASET=pathlib.Path("./vcf_dataset")
    else:
        DATASET=pathlib.Path(f"./{dataset}")
    if DATASET.exists():
        shutil.rmtree(DATASET)
        return (dbc.Alert("Dataset already exist. Terminatiing the process for now", color="danger"))
    else:
        df = create(DATASET, FILES_DIRECTORY)
        return(dbc.Alert("Dataset has been created successfully", color="success")
               )

def create(dataset_path, files_directory):
    ingested_files_count = 0
    files = list(files_directory.glob("*.vcf.gz"))
    dataset = tiledbvcf.Dataset(str(dataset_path),"w")
    dataset.create_dataset()
    for file in files:
        try:
            dataset.ingest_samples([str(file)])
            ingested_files_count = ingested_files_count + 1
        except Exception as e:
            print(e)
    return(dataset)






