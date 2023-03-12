"""
    Module containing the dash tab for the charts of the last GP
"""

from dash import html

from . import utils


def GeneralTab() -> html.Div:
    """ This function returns the general tab as a Div """
    return html.Div([
        # body
        html.Div(id=utils.GENERAL_BODY, className=utils.BODY_CLASS, children=[
            # left widget
            html.Div(id=utils.GENERAL_LEFT_WIDGET, className=utils.WIDGET_CLASS, children=[]),  # TODO: add the charts

            # right widget
            html.Div(id=utils.GENERAL_RIGHT_WIDGET, className=utils.WIDGET_CLASS, children=[])  # TODO: add the charts
        ])
    ])
