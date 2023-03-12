"""
    Module containing the dash tab for the charts of the last GP
"""

from dash import html

from . import utils


def LastGPTab() -> html.Div:
    """ This function returns the last GP tab as a Div """
    return html.Div([
        # title bar
        html.Div(id=utils.LAST_GP_TITLE_BAR, children=[
            html.H1(" ")]),  # TODO: add the name of the last GP

        # body
        html.Div(id=utils.LAST_GP_BODY, className=utils.BODY_CLASS, children=[
            # left widget
            html.Div(id=utils.LAST_GP_LEFT_WIDGET, className=utils.WIDGET_CLASS, children=[]),  # TODO: add the charts

            # right widget
            html.Div(id=utils.LAST_GP_RIGHT_WIDGET, className=utils.WIDGET_CLASS, children=[])  # TODO: add the charts
        ])
    ])
