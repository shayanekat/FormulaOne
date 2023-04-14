"""
    Module containing the dash tab for the charts of the last GP
"""

from dash import html

from . import utils
from .backend import general


def GeneralTab() -> html.Div:
    """ This function returns the general tab as a Div """
    return html.Div([
        # body
        html.Div(id=utils.GENERAL_BODY, className=utils.BODY_CLASS, children=[
            # left widget
            html.Div(id=utils.GENERAL_LEFT_WIDGET, className=utils.WIDGET_CLASS,
                     children=general.cumulative_points(), style=utils.WIDGET_STYLE),

            # right widget
            html.Div(id=utils.GENERAL_RIGHT_WIDGET, className=utils.WIDGET_CLASS,
                     children=general.heatmaps(), style=utils.WIDGET_STYLE)
        ], style=utils.BODY_STYLE)
    ], style=utils.BODY_STYLE)
