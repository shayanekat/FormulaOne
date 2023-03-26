"""
    Main dashboard app
"""
from dash import Dash, dcc, html

from sources import utils
from sources.battles_tab import BattlesTab
from sources.circuits_tab import CircuitsTab
from sources.general_tab import GeneralTab
from sources.last_gp_tab import LastGPTab


def main():
    """ Main function of the app """
    app = Dash("Formula 1 Dashboard")
    app.title = "Formula 1 Dashboard"
    app.layout = html.Div(
        dcc.Tabs(id="tabs", value="tab-1", children=[
            dcc.Tab(label="Dernier GP", value="tab-last-gp", id=utils.LAST_GP_TAB, className="tab_bar", children=LastGPTab()),
            dcc.Tab(label="Général", value="tab-general", id=utils.GENERAL_TAB, className="tab_bar", children=GeneralTab()),
            dcc.Tab(label="Batailles", value="tab-battles", id=utils.BATTLES_TAB, className="tab_bar", children=BattlesTab()),
            dcc.Tab(label="Circuits", value="tab-circuits", id=utils.CIRCUITS_TAB, className="tab_bar", children=CircuitsTab())]
        )
    )

    app.run()

if __name__ == "__main__":
    main()