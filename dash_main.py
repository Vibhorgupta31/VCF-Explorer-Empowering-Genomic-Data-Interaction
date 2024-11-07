from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf

import createDataset
from dash_app import app
#from dataset_creation import layout as dataset_creation_layout
from dataset_filtering import layout as dataset_filtering_layout
from needle_plot import layout as dataset_plot_layout
from createDataset import create_dataset as create_dataset
from flask import g
from dash_core_components  import Store

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "fontFamily":"Courier"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("VCF Explorer", className="display-4"),
        html.Hr(),
        html.P(
            "Prototype", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("About", href="/", active="exact"),
                dbc.NavLink("Create dataset", href="/page-1", active="exact"),
                dbc.NavLink("Filter", href="/page-2", active="exact"),
                dbc.NavLink("Visualization", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return about_page
    elif pathname == "/page-1":
        return create_dataset
    elif pathname == "/page-2":
        return dataset_filtering_layout
    elif pathname == "/page-3":
        return dataset_plot_layout
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

about_page = html.Div([html.H2("Introduction", style={"textAlign": "Left", "fontFamily":"Courier"}),
                       html.P("Variant Calling Files (.vcf) are essential in genomics, encoding valuable information about genetic variants that may influence phenotypic traits. Analyzing these files is pivotal for Genome-Wide Association Studies (GWAS), population genetics, and other genetic research.",style={"textAlign": "Justify", "fontFamily":"Courier"}),
                       html.P("While working extensively with VCF files, we identified a gap: current tools are often limited, outdated, or have specific shortcomings that restrict efficient analysis. This motivated us to create a robust solution—VCF Explorer. ",style={"textAlign": "Justify", "fontFamily":"Courier"}),
                       html.P("Our platform enables users to create and manage VCF datasets using a powerful vector-based backend powered by TileDB. Users can query, annotate, interact with, and visualize their data seamlessly. With VCF Explorer, we aim to provide an open-source, flexible, and user-friendly tool that can be easily downloaded, customized, and scaled to meet diverse research needs",
                              style={"textAlign": "Justify", "fontFamily":"Courier"}),
                       html.H3("Acknowledgements", style={"textAlign": "Left", "fontFamily":"Courier"}),
                       html.Ul(children=[
                           html.Li("TileDB-VCF", style={"textAlign": "Left", "fontFamily":"Courier"}),
                           html.Li("Lineberger Comprehsensive Care Center, UNC", style={"textAlign": "Left", "fontFamily":"Courier"})]
                       ),
                       html.H3("Created by:", style={"textAlign": "Left", "fontFamily":"Courier"}),
                       html.Ul(children=[
                           html.Li("Sarang Bhutada", style={"textAlign": "Left", "fontFamily": "Courier"}),
                           html.Li("Vibhor Gupta",
                                   style={"textAlign": "Left", "fontFamily": "Courier"})]
                       )
                       ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8095)