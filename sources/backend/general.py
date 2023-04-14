"""
    This module contains all data processing and graphing functions for the General tab
"""

import json

import pandas as pd
import plotly.express as px
from dash import dcc

# Import data
data_all = pd.read_json('data/data_2023.json')
data_all["index"] = data_all.groupby("pilot").cumcount()
data_all["index"] += 1
data_all["improvement"] = data_all["grid"] - data_all["result"]

# Dataset of the cumulative points of each pilot
data_points = data_all[["pilot", "points", "circuit_name"]].copy()
data_points["cum_points"] = data_points.groupby("pilot").cumsum()
data_points["index"] = data_points.groupby("pilot").cumcount()

# Extraction of pilots per team
with open("sources/utilites/teams_2023.json", encoding="utf8") as jsonfile:
    teams_pilot = json.load(jsonfile)

data_team_points = {"team": [], "points": [], "cum_points": [], "index": [], "circuit_name": []}
for i in data_points["index"].unique():
    for team in teams_pilot:
        data_team_points["team"].append(team)
        data_team_points["points"].append(data_points[data_points["index"] == i][data_points["pilot"].isin(teams_pilot[team])]["points"].sum())
        data_team_points["cum_points"].append(data_points[data_points["index"] == i][data_points["pilot"].isin(teams_pilot[team])]["cum_points"].sum())
        data_team_points["index"].append(i)
        data_team_points["circuit_name"].append(data_points[data_points["index"] == i]["circuit_name"].unique()[0])
data_team_points = pd.DataFrame(data_team_points)

# colors
with open("sources/utilites/colors.json", encoding="utf8") as jsonfile:
    colors = json.loads(jsonfile.read())

# dnf count per pilot and per team (1 = dnf, 0 = not dnf)
pilot_dnf_count = data_all[data_all["dnf"] == 1]["pilot"].value_counts()
pilot_dnf_count = pd.DataFrame({"pilot": list(pilot_dnf_count.index),
                                "dnf": list(pilot_dnf_count.values)})
team_dnf_count = data_all[data_all["dnf"] == 1]["team"].value_counts()
team_dnf_count = pd.DataFrame({"team": list(team_dnf_count.index),
                               "dnf": list(team_dnf_count.values)})

def cumulative_points() -> list[dcc.Graph]:
    """ Function that returns the graphs of the General tab for the cumulative points section """
    pilots_cum_points = px.line(data_points, x="index", y="cum_points", color="pilot",
                                title="Pilots cumlated points", template="plotly_dark",
                                markers=True)

    team_cum_points = px.line(data_team_points, x="index", y="cum_points", color="team",
                              title="Teams cumulated points", template="plotly_dark", markers=True)

    return [
        dcc.Graph(figure=pilots_cum_points),
        dcc.Graph(figure=team_cum_points)
    ]

def heatmaps() -> list[dcc.Graph]:
    """ Function that returns the graphs of the General tab for the heatmaps section """
    pilots_grid_pos = px.density_heatmap(data_all, x="pilot", y="grid",
                                         title="Pilot's grid position", nbinsx=20, nbinsy=20,
                                         template="plotly_dark")

    pilots_results_pos = px.density_heatmap(data_all, x="pilot", y="result", nbinsx=20, nbinsy=20,
                                            title="Pilot's result position", template="plotly_dark")

    pilots_dnf = px.density_heatmap(data_all, x="pilot", y="dnf", nbinsx=20, nbinsy=2,
                                      title="Pilot's DNF", template="plotly_dark")

    teams_dnf = px.density_heatmap(data_all, x="team", y="dnf", nbinsx=10, nbinsy=2,
                                   title="Team's DNF", template="plotly_dark")

    return [
        dcc.Graph(figure=pilots_grid_pos),
        dcc.Graph(figure=pilots_results_pos),
        dcc.Graph(figure=pilots_dnf),
        dcc.Graph(figure=teams_dnf)
    ]
