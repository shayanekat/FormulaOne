"""
    first app runned to download the data
"""

import json
from tkinter import *

import requests

from sources import app, utils

# ===== backend =====
# global variables
with open("cache.txt") as file:
    n = int(file.read())
LAP_LINK = "http://ergast.com/api/f1/2023/"+str(n)+"/laps.json?limit=10000"
DATA_LINK = "http://ergast.com/api/f1/2023/"+str(n)+"/results.json"
SPRINT_LINK = "http://ergast.com/api/f1/2023/"+str(n)+"/sprint.json"

# button hover
def on_ba_enter(e):
    b_availaible['background'] = utils.SELECTED_TAB

def on_ba_leave(e):
    b_availaible['background'] = utils.NOT_SELECTED_TAB

def on_bd_enter(e):
    b_download['background'] = utils.SELECTED_TAB

def on_bd_leave(e):
    b_download['background'] = utils.NOT_SELECTED_TAB

# buttons function
def are_data_avalaible():
    req_lap = requests.get(LAP_LINK)
    filename_lap = req_lap.url[LAP_LINK.rfind('/')+1:]
    dict_data = json.loads(req_lap.text)
    if len(dict_data["MRData"]["RaceTable"]["Races"]) > 0:
        error_label.config(text="Data are avalaible")
    else:
        error_label.config(text="Data are not avalaible")

def download_data():
    with open("id2code.json") as file:
        id2code = json.load(file)
    with open("sources/utilities/teams_2023.json") as file:
        teams = json.load(file)

    def get_team(code: str):
        """
        Fonction qui retourne l'équipe d'un pilote

        Args:
            code (str): le trois lettres du nom du pilote

        Returns:
            str: le nom de l'équipe
        """
        for team, pilot in teams.items():
            if code in pilot:
                return team

    # Générer l'url
    with open("cache.txt") as file:
        n = int(file.read())

    # Trouver et télécharger le fichier
    req_data = requests.get(DATA_LINK)
    filename_data = req_data.url[DATA_LINK.rfind('/')+1:]
    req_sprint = requests.get(SPRINT_LINK)
    filename_sprint = req_sprint.url[SPRINT_LINK.rfind('/')+1:]

    # extraire les précédentes données
    with open("data/data_2023.json") as file:
        previous = json.load(file)

    # ==== extraire les données des grands prix ====
    # Choisir les bonnes données
    dict_data = json.loads(req_data.text)
    data = dict_data["MRData"]["RaceTable"]["Races"][0]["Results"]

    circuit_name = dict_data["MRData"]["RaceTable"]["Races"][0]["Circuit"]["circuitId"]

    # Extraction des nouvelles données
    for i, v in enumerate(data):
        # Nom du pilote
        drv = data[i]["Driver"]["code"].lower()

        # Vitesse
        try:
            speed = data[i]["FastestLap"]["AverageSpeed"]["speed"]
        except KeyError:
            speed = "nan"

        # Temps meilleur tour
        try:
            lap_time = data[i]["FastestLap"]["Time"]["time"]
            lap_time = lap_time.split(":")
            l_t = str(int(lap_time[0])*60 + float(lap_time[1]))
        except KeyError:
            l_t = "nan"

        # Grille de départ
        try:
            grid = data[i]["grid"]
        except KeyError:
            grid = "nan"

        # Points
        pts = data[i]["points"]
        if len(json.loads(req_sprint.text)["MRData"]["RaceTable"]["Races"]) > 0:
            for j in range(len(json.loads(req_sprint.text)["MRData"]["RaceTable"]["Races"][0]["SprintResults"])):
                pts = str(int(pts) + int(json.loads(req_sprint.text)["MRData"]["RaceTable"]["Races"][0]["SprintResults"][j]["points"])) if json.loads(req_sprint.text)["MRData"]["RaceTable"]["Races"][0]["SprintResults"][j]["Driver"]["code"].lower() == drv else pts

        # Classement
        try:
            pos = data[i]["position"]
        except KeyError:
            pos = "nan"

        # Temps
        try:
            tps = str(int(data[i]["Time"]["millis"])/1000)
        except KeyError:
            tps = "nan"

        dnf = 0 if data[i]["status"] == "Finished" or "Lap" in data[i]["status"] else 1  # 0: terminé, 1: abandon

        # Ajout de la ligne au données
        previous["pilot"].append(drv)
        previous["team"].append(get_team(drv))
        previous["avg_speed"].append(speed)
        previous["best_lap"].append(l_t)
        previous["grid"].append(grid)
        previous["points"].append(pts)
        previous["result"].append(pos)
        previous["time"].append(tps)
        previous["circuit_name"].append(circuit_name)
        previous["dnf"].append(dnf)

    # ==== extraire les données des tours ====
    laps = {"pilot": [], "team": [], "lap": [], "time": [], "position": []}
    # extraire les données des tours
    lap_link = "http://ergast.com/api/f1/2023/"+str(n)+"/laps.json?limit=10000"
    req_lap = requests.get(lap_link)
    filename_lap = req_lap.url[lap_link.rfind('/') + 1:]

    # Choisir les bonnes données
    data = json.loads(req_lap.text)["MRData"]["RaceTable"]["Races"][0]["Laps"]
    for i, v in enumerate(data):
        # mettre les données dans le dictionnaire
        for j in range(len(data[i]["Timings"])):
            laps["lap"].append(i+1)
            laps["pilot"].append(id2code[data[i]["Timings"][j]["driverId"]])
            laps["team"].append(get_team(id2code[data[i]["Timings"][j]["driverId"]]))
            laps["time"].append(str(int(data[i]["Timings"][j]["time"].split(":")[0])*60 + float(data[i]["Timings"][j]["time"].split(":")[1])))
            laps["position"].append(j+1)

    # # mettre a jour les données
    with open("data/lap_data.json", "w") as file:
        json.dump(laps, file)
    with open("data/data_2023.json", "w") as file:
        json.dump(previous, file)

    # extraction des données entrées par l'utilisateur
    with open("data/circuit_2023.json") as file:
        circuit = json.load(file)
    circuit["name"].append(name_e.get())
    circuit["length"].append(int(length_e.get()))
    circuit["turn nb"].append(int(turn_e.get()))
    circuit["lap nb"].append(int(lap_e.get()))
    circuit["lat"].append(float(lat_e.get()))
    circuit["long"].append(float(long_e.get()))
    circuit["alt"].append(int(alt_e.get()))
    with open("data/circuit_2023.json", "w") as file:
        json.dump(circuit, file)

    # Mettre le cache à jour
    n += 1
    with open("cache.txt", "w") as file:
        file.write(str(n))

    # lancer le serveur du site
    app.main()


# ===== frontend =====
root = Tk()
root.title("Data Downloader")
root.configure(background=utils.BODY_BACKGROUND)

b_availaible = Button(root, text="Are data avalaible", bg=utils.NOT_SELECTED_TAB)
b_availaible.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
error_label = Label(root, text=" ", bg=utils.BODY_BACKGROUND, fg="white")
error_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

name_l = Label(root, text="Circuit name : ", bg=utils.BODY_BACKGROUND, fg="white")
name_l.grid(row=2, column=0, padx=10, pady=10)
name_e = Entry(root, bg="black", fg="white")
name_e.grid(row=2, column=1, padx=10, pady=10)

length_l = Label(root, text="Circuit length : ", bg=utils.BODY_BACKGROUND, fg="white")
length_l.grid(row=3, column=0, padx=10, pady=10)
length_e = Entry(root, bg="black", fg="white")
length_e.grid(row=3, column=1, padx=10, pady=10)

lap_l = Label(root, text="Number of laps : ", bg=utils.BODY_BACKGROUND, fg="white")
lap_l.grid(row=4, column=0, padx=10, pady=10)
lap_e = Entry(root, bg="black", fg="white")
lap_e.grid(row=4, column=1, padx=10, pady=10)

turn_l = Label(root, text="Number of turns : ", bg=utils.BODY_BACKGROUND, fg="white")
turn_l.grid(row=5, column=0, padx=10, pady=10)
turn_e = Entry(root, bg="black", fg="white")
turn_e.grid(row=5, column=1, padx=10, pady=10)

lat_l = Label(root, text="Latitude : ", bg=utils.BODY_BACKGROUND, fg="white")
lat_l.grid(row=6, column=0, padx=10, pady=10)
lat_e = Entry(root, bg="black", fg="white")
lat_e.grid(row=6, column=1, padx=10, pady=10)

long_l = Label(root, text="Longitude : ", bg=utils.BODY_BACKGROUND, fg="white")
long_l.grid(row=7, column=0, padx=10, pady=10)
long_e = Entry(root, bg="black", fg="white")
long_e.grid(row=7, column=1, padx=10, pady=10)

alt_l = Label(root, text="Altitude : ", bg=utils.BODY_BACKGROUND, fg="white")
alt_l.grid(row=8, column=0, padx=10, pady=10)
alt_e = Entry(root, bg="black", fg="white")
alt_e.grid(row=8, column=1, padx=10, pady=10)

b_download = Button(root, text="Download data", bg=utils.NOT_SELECTED_TAB)
b_download.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
