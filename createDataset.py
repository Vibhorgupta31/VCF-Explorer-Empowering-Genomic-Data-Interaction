# Library Imports
from dash import Dash,html,dcc, Input, Output, State,callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pathlib
import tiledbvcf
import shutil




create_dataset = html.Div([
    dbc.Label("Directory to VCF Files: "),
    dcc.Input(id = "files_directory", placeholder="Directory containing VCF files"),
    html.Br(),
    dbc.Label("Dataset Name: "),
    dcc.Input(id = "dataset", placeholder="Dataset Name ( Default : vcf_dataset )"),
    html.Button('Submit', id='constants_update_submit', n_clicks=0),
    html.P(id="Output")
])

@callback(Output("Output", component_property="children"),
          Input("constants_update_submit", component_property="n_clicks"),
          State("dataset", component_property="value"),
          State("files_directory", component_property="value"))
def creation(n_clicks, dataset, files_directory):
    if n_clicks == 0:
        raise PreventUpdate
    FILES_DIRECTORY = pathlib.Path(files_directory)
    if FILES_DIRECTORY.exists() == False:
        return ("File path doesn't exist")
    if len(dataset) == 0:
        DATASET = pathlib.Path("./vcf_dataset")
    else:
        DATASET = pathlib.Path(f"./{dataset}")

    if DATASET.exists():
        return (html.P("Dataset Already exist. Please select what you want to do next ?"),
                dcc.Dropdown(["Remove", "Update"], id="duplicate_dataset_case"),
                html.Button('Submit', id='ddbutton', n_clicks=0),
                html.P(id="output_message"))
    else:
        df = create(DATASET, FILES_DIRECTORY)
        return (df)

def create(dataset_path, files_directory):
    ingested_files_count = 0
    files = list(files_directory.glob("*.vcf.gz"))
    dataset = tiledbvcf.Dataset(str(dataset_path),"w")
    dataset.create_dataset()
    print(f"The directory has {len(files)} vcf files")
    print("Files ingestion started")
    for file in files:
        try:
            dataset.ingest_samples([str(file)])
            ingested_files_count = ingested_files_count + 1
        except Exception as e:
            print(e)
    print(f"{ingested_files_count} out of {len(files)} ingested")
    return(dataset)

