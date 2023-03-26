"""
    This module contains all data processing and graphing functions for the last GP tab
"""

import json

import pandas as pd
import plotly.express as px
from dash import dcc

# ===== DATA PROCESSING =====
# Import data
data_all = pd.read_json('data/data_2023.json')
data_all["index"] = data_all.groupby("pilot").cumcount()
data_all["index"] += 1
data_all["improvement"] = data_all["grid"] - data_all["result"]

# last gp
last_gp = data_all.groupby("pilot").tail(1)

# colors
with open("sources/utilites/colors.json", "r", encoding="utf8") as file:
    colors = json.loads(file.read())

# lap of last gp
lap_df = pd.read_json("data/lap_data.json")

# average lap time of each pilot on last gp
dico = {pilot: lap_df.groupby("pilot").mean()["time"][pilot] for pilot in lap_df["pilot"].unique()}
last_gp["average_lap_time"] = last_gp["pilot"].map(dico)


# ===== GRAPHS =====
def pilot_comparison() -> list[dcc.Graph]:
    """ Function that returns the graphs of the last GP tab for the pilot comparison section """
    fig_fastest_laptime = px.scatter(last_gp, x="pilot", y="best_lap",
                                     title="Time of fastest lap of each pilot (s)",
                                     marginal_y="histogram", template="plotly_dark")

    fig_avg_laptime = px.scatter(last_gp, x="pilot", y="average_lap_time",
                                 title="Average lap time of each pilot (s)", marginal_y="histogram",
                                 template="plotly_dark")

    fig_fastest_ag_speed = px.scatter(last_gp, x="pilot", y="avg_speed",
                                      title="Mean speed of the fastes_lap of each pilot (kmh)",
                                      marginal_y="histogram", template="plotly_dark")

    fig_total_time = px.scatter(last_gp, x="pilot", y="time", title="Total time (s)",
                                marginal_y="histogram", template="plotly_dark") # no data displayed if the pilot didn't finish or had one lap of delay

    fig_improvement = px.bar(last_gp, x="pilot", y="improvement", title="Improvement of the pilots",
                             color="pilot", color_discrete_map=colors["pilot"],
                             template="plotly_dark")

    return [
        dcc.Graph(figure=fig_fastest_laptime, id="fastest-laptime"),
        dcc.Graph(figure=fig_avg_laptime, id="avg-laptime"),
        dcc.Graph(figure=fig_fastest_ag_speed, id="fastest-avg-speed"),
        dcc.Graph(figure=fig_total_time, id="total-time"),
        dcc.Graph(figure=fig_improvement, id="improvement")
    ]

def lap_data() -> list[dcc.Graph]:
    """ Function that returns the graphs of the last GP tab for the lap data section """
    fig_laptime = px.line(lap_df, x="lap", y="time", color="pilot",
                          color_discrete_map=colors["pilot"],
                          title="Lap time evolution along the race",
                          markers=True, template="plotly_dark")

    fig_position = px.line(lap_df, x="lap", y="position", color="pilot",
                                 color_discrete_map=colors["pilot"],
                                 title="Pilot's position along the race",
                                 markers=True, template="plotly_dark")
    fig_position.update_layout(yaxis={'autorange': 'reversed'})

    fig_position_density = px.density_heatmap(lap_df, x="pilot", y="position", nbinsx=20, nbinsy=20,
                                              title="Postion of each pilot during the race",
                                              template="plotly_dark")

    return [
        dcc.Graph(figure=fig_laptime, id="laptime"),
        dcc.Graph(figure=fig_position, id="position"),
        dcc.Graph(figure=fig_position_density, id="position-density")
    ]
