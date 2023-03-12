"""
    Module containing the dash tab for the charts of the circuits
"""

from dash import html

from . import utils


def CircuitsTab() -> html.Div:
    """ This function returns the circuits tab as a Div """
    return html.Div([
        # body
        html.Div(id=utils.CIRCUITS_BODY, className=utils.BODY_CLASS, children=[
            # left widget
            html.Div(id=utils.CIRCUITS_LEFT_WIDGET, className=utils.WIDGET_CLASS, children=[]),  # TODO: add the charts

            # right widget
            html.Div(id=utils.CIRCUITS_RIGHT_WIDGET, className=utils.WIDGET_CLASS, children=[])  # TODO: add the charts
        ])
    ])
