import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc

# Import data
data_all = pd.read_json('data/data_2023.json')
data_all["index"] = data_all.groupby("pilot").cumcount()
data_all["index"] += 1
data_all["improvement"] = data_all["grid"] - data_all["result"]

# colors
colors = json.loads(open("sources/utilites/colors.json").read())

# circuit data
circuit_df = pd.read_json("data/circuit_2023.json")
circuit_df["lap length"] = circuit_df["lap nb"] * circuit_df["length"]
circuit_df["ratio"] = circuit_df["lap length"] / circuit_df["turn nb"]

def MainData() -> list[dcc.Graph]:
    """ Function that returns the graphs of the main data filtered by circuit """
    fig_avg_speed_fastest_lap = go.Figure(layout=go.Layout(title="Circuit average speed on fastest laps", template="plotly_dark"))
    fig_avg_speed_fastest_lap.add_traces(go.Box(x=data_all["circuit_name"], y=data_all["avg_speed"], text=data_all["pilot"], boxpoints="all", jitter=0.1, pointpos=0, boxmean=True))
    
    return [
        dcc.Graph(figure=fig_avg_speed_fastest_lap)
    ]

def CircuitData() -> list[dcc.Graph]:
    """ Function that returns the graphs of the circuits data """
    fig_circuit_length = go.Figure(layout=go.Layout(title="Circuit Length", template="plotly_dark"))
    fig_circuit_length.add_trace(go.Box(y=circuit_df["length"], name="boxplot circuit length", boxpoints="all", jitter=0.1, pointpos=0, boxmean=True, text=circuit_df["name"]))
    
    fig_lap_nb = go.Figure(layout=go.Layout(title="Circuit Lap Number", template="plotly_dark"))
    fig_lap_nb.add_traces(go.Box(y=circuit_df["lap nb"], name="boxplot number of lap", boxpoints="all", jitter=0.1, pointpos=0, boxmean=True))

    fig_circuit_map = px.scatter_geo(circuit_df, lat="lat", lon="long", hover_name="name", title="Circuit Location", template="plotly_dark")
    
    fig_race_distance = go.Figure(layout=go.Layout(title="Lap number vs length", template="plotly_dark"))
    fig_race_distance.add_traces(go.Scatter(x=circuit_df["lap nb"], y=circuit_df["length"], mode="markers", text=circuit_df["name"], name="circuit data"))
    fig_race_distance.add_traces(go.Line(x=[i for i in range(30, 80)], y=[300000/i for i in range(30, 80)], name="expected tendancy"))
    
    return [
        dcc.Graph(figure=fig_circuit_length),
        dcc.Graph(figure=fig_lap_nb),
        dcc.Graph(figure=fig_circuit_map),
        dcc.Graph(figure=fig_race_distance)
    ]
