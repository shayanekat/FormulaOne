import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


# generate graphs
fig = make_subplots(rows=7, cols=1, subplot_titles=(
    "rythme moyen par pilote",
    "evolution du rythme",
    "evolution des positions",
    "points pilotes",
    "point ecuries",
    "evolution de la grille",
    "evolution des resultats"
    )
)

fig.add_trace(
    go.Scatter(x=last_gp["pilot"], y=last_gp["avg_lap_time"], name="rythme moyen par pilote"),
    row=1, col=1)

fig.add_trace(
    go.Line(x=last_gp["pilot"], y=last_gp["average_lap_time"], name="evolution du rythme"),
    row=2, col=1)

fig.add_trace(
    go.Line(x=last_gp["pilot"], y=last_gp["position"], name="evolution des positions"),
    row=3, col=1)

fig.add_trace(
    go.Line(x=data_points["circuit_name"], y=data_points["cum_points"], name="points pilotes"),
    row=4, col=1)

fig.add_trace(
    go.Line(x=data_team_points["circuit_name"], y=data_team_points["cum_points"], name="points ecuries"),
    row=5, col=1)

fig.add_trace(
    go.Line(x=df_data["circuit_name"], y=df_data["grid"], name="evolution de la grille"),
    row=6, col=1)

fig.add_trace(
    go.Line(x=df_data["circuit_name"], y=df_data["result"], name="evolution des resultats"),
    row=7, col=1)

fig.update_layout(title_text="Analyse des données de F1 2024", template="plotly_dark")

fig.show()
    
