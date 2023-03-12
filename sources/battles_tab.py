"""
    Module containing the dash tab for the charts of the battles
"""

from dash import html

from . import utils


def BattlesTab() -> html.Div:
    """ This function returns the battles tab as a Div """
    return html.Div([
        # body
        html.Div(id=utils.BATTLES_BODY, className=utils.BODY_CLASS, children=[
            # left widget
            html.Div(id=utils.BATTLES_LEFT_WIDGET, className=utils.WIDGET_CLASS, children=[]),  # TODO: add the charts

            # right widget
            html.Div(id=utils.BATTLES_RIGHT_WIDGET, className=utils.WIDGET_CLASS, children=[])  # TODO: add the charts
        ])
    ])
