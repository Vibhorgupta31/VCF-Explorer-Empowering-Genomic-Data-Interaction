from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
import pathlib
import tiledbvcf
from dash_app import app
from dataset_creation import layout as dataset_creation_layout
from dataset_filtering import layout as dataset_filtering_layout
from needle_plot import layout as dataset_plot_layout


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
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
                dbc.NavLink("Filter dataset", href="/page-2", active="exact"),
                dbc.NavLink("Needle plot", href="/page-3", active="exact"),
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
        return html.P("Intro about the project")
    elif pathname == "/page-1":
        return dataset_creation_layout
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

if __name__ == "__main__":
    app.run_server(debug=True, jupyter_mode = 'external', port=8052)