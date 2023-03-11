"""
    Main dashboard app
"""
from dash import Dash, dcc, html


def main():
    app = Dash(style_sheet="sources/utilites/style.css")
    app.title = "Formula 1 Dashboard"
    app.layout = html.Div(
        dcc.Tabs(id="tabs", value="tab-1", children=[
            dcc.Tab(label="Général", value="tab-general")]
        )
    )

    app.run()
