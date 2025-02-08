import json
import time

import pandas as pd
import requests

DT = 1 # delay time in seconds to avoid API rate limit

def update_data(race_year, race_index):
    # get existing data
    df = pd.read_csv("data2025.csv")

    # case no new data
    if race_index in df.index:
        print("No new data")

    # case new data
    else:
        print("New data")
        # init
        if len(df) == 0:
            lastIndex = 0
        else:
            lastIndex = max(df["raceIndex"])
        
        # old data
        strdata = df.to_dict()
        
        while lastIndex < race_index:
            lastIndex += 1
            # get new data from API from last index to race_index (inclusive)
            # -> quali
            qualy_url = f"https://ergast.com/api/f1/{race_year}/{lastIndex}/qualifying.json"
            qualy_req = requests.get(qualy_url)
            qualy_dict = qualy_req.json()
            
            # -> standing
            standings_url = f"http://ergast.com/api/f1/{race_year}/{lastIndex}/driverStandings.json"
            standings_req = requests.get(standings_url)
            standings_dict = standings_req.json()
            
            # -> result
            result_url = f"http://ergast.com/api/f1/{race_year}/{lastIndex}/results.json"
            result_req = requests.get(result_url)
            result_dict = result_req.json()
        
            # merge new data with existing data
            records = []
            # -> quali
            quali_data = qualy_dict["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
            for i in range(len(quali_data)):
                record = {}
                record["raceIndex"] = lastIndex
                record["driver"] = quali_data[i]["Driver"]["code"]
                record["quali"] = quali_data[i]["position"]
                records.append(record)
            
            # -> standing
            standing_data = standings_dict["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            for i in range(len(standing_data)):
                # find the corresponding record by driver
                for j in range(len(records)):
                    if records[j]["driver"] == standing_data[i]["Driver"]["code"]:
                        records[j]["points"] = standing_data[i]["points"]
                        break
                else:
                    record = {}
                    record["raceIndex"] = lastIndex
                    record["driver"] = standing_data[i]["Driver"]["code"]
                    records.append(record)
                    j = len(records) - 1
                
                records[j]["standing"] = standing_data[i]["points"]
                
            # -> result
            result_data = result_dict["MRData"]["RaceTable"]["Races"][0]["Results"]
            for i in range(len(result_data)):
                # find the corresponding record by driver
                for j in range(len(records)):
                    if records[j]["driver"] == result_data[i]["Driver"]["code"]:
                        records[j]["result"] = result_data[i]["position"]
                        break
                else:
                    record = {}
                    record["raceIndex"] = lastIndex
                    record["driver"] = result_data[i]["Driver"]["code"]
                    records.append(record)
                    j = len(records) - 1
                
                records[j]["result"] = result_data[i]["position"]
            
        # save data to data.csv
        print("Saving data")
        for record in records:
            df.loc[-1] = record
            df.index = df.index + 1
            df = df.sort_index()
        df.to_csv("data2025.csv", index=False)
    
    return df