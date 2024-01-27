import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from plotly.subplots import make_subplots

import data_download

# data update
ask = input("Voulez vous mettre à jour les données ? (y/n) ")
if ask == "y":
    YEAR = 2024
    data_url, sprint_url = data_download.get_urls(YEAR)
    dataget = data_download.get_data_links(data_url)
    sprintget = data_download.get_data_links(sprint_url)
    data_download.data_update(dataget, sprintget)
    data_download.update_lap_data(YEAR)
    data_download.update_cache()

# load data
df_data = pd.read_json("data_2024.json")

last_gp = df_data.groupby("pilot").tail(1)
df_lap = pd.read_json("lap_data.json")
dico = {pilot: df_lap.groupby("pilot").mean()["time"][pilot] for pilot in df_lap["pilot"].unique()}
last_gp["average_lap_time"] = last_gp["pilot"].map(dico)

data_points = df_data[["pilot", "points", "circuit_name"]].copy()
data_points["cum_points"] = data_points.groupby("pilot").cumsum()
data_points["index"] = data_points.groupby("pilot").cumcount()

data_team_points = {"team": [], "points": [], "cum_points": [], "index": [], "circuit_name": []}
for i in data_points["index"].unique():
    for team in data_download.teams.keys():
        data_team_points["team"].append(team)
        data_team_points["points"].append(data_points[data_points["index"] == i][data_points["pilot"].isin(data_download.teams[team])]["points"].sum())
        data_team_points["cum_points"].append(data_points[data_points["index"] == i][data_points["pilot"].isin(data_download.teams[team])]["cum_points"].sum())
        data_team_points["index"].append(i)
        data_team_points["circuit_name"].append(data_points[data_points["index"] == i]["circuit_name"].unique()[0])
data_team_points = pd.DataFrame(data_team_points)

with open("colors.json", encoding="utf8") as file:
    colors = json.load(file)

# generate graphs
fig_pace = px.scatter(last_gp, x="pilot", y="average_lap_time", title="rythme moyen par pilote", template="plotly_dark")
fig_pace_evol = px.line(df_lap, x="lap", y="time", title="evolution du rythme", template="plotly_dark", color="pilot", color_discrete_map=colors["pilot"]) 
fig_pos_evol = px.line(df_lap, x="lap", y="position", title="evolution des positions", template="plotly_dark", color="pilot", color_discrete_map=colors["pilot"])
fig_pilot_points = px.line(data_points, x="circuit_name", y="cum_points", title="points pilote", template="plotly_dark", color="pilot", color_discrete_map=colors["pilot"]) 
fig_team_points = px.line(data_team_points, x="circuit_name", y="cum_points", title="points ecurie", template="plotly_dark", color="team") 
fig_grid = px.line(df_data, x="circuit_name", y="grid", title="evolution de la grille", template="plotly_dark", color="pilot", color_discrete_map=colors["pilot"]) 
fig_res = px.line(df_data, x="circuit_name", y="result", title="evolution des resultats", template="plotly_dark", color="pilot", color_discrete_map=colors["pilot"]) 

app = Dash("Formula 1 Data Analysis - 2024 Edition")

app.layout = html.Div([
    dcc.Graph(id="pace", figure=fig_pace),
    dcc.Graph(id="pace_evol", figure=fig_pace_evol),
    dcc.Graph(id="pos_evol", figure=fig_pos_evol),
    dcc.Graph(id="pilot_points", figure=fig_pilot_points),
    dcc.Graph(id="team_points", figure=fig_team_points),
    dcc.Graph(id="grid", figure=fig_grid),
    dcc.Graph(id="res", figure=fig_res)
])

if __name__ == '__main__':
    app.run(debug=True)