import pandas as pd
from datawrappergraphics.Map import *
import requests


states = pd.read_html("https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971")[0]
charts = pd.read_csv("graphics.csv")

raw = pd.read_csv("assets/data/data-guns.csv")
raw = raw.set_index("STATE").join(states.set_index("Alpha code")).reset_index()

data = raw.copy()

data = data.loc[data["YEAR"] == 2020, :].set_index("State").join(charts.set_index("state")).reset_index()

data["image_link"] = "<img src='http://img.datawrapper.de/" + data["chart_id"] + "/tiny.png' width='200px'>"
data["label"] = data["index"] + "<br>" + data["RATE"].astype(str)

print(data)
data.to_clipboard()


# state_graphics = []


# for state in ["Virginia", "Washington", "Wisconsin", "West Virginia", "Wyoming", "Vermont"]:
#     print(state)
#     state_data = raw.loc[raw["State"] == state, ["YEAR", "RATE"]].sort_values("YEAR").loc[raw["YEAR"] != 2005, :].set_index("YEAR")
#     linechart = dwmaps.Chart(copy_id="s8lzT").data(state_data).head(f"Gun violence in {state}").publish()
#     print(linechart.CHART_ID)
#     record = pd.DataFrame({"state": [state], "chart_id": [linechart.CHART_ID]})
#     state_graphics.append(record)
    
# records = pd.concat(state_graphics)
# records = pd.concat([states, records])

# print(records)

# payload = {
#     "ids": records["chart_id"].to_list(),
#     "patch": {"folderId": "104558"}
#     }

# headers = {
#     "Accept": "*/*",
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer HQd4kFqSSQyh5I7dK7YKNonyG74UpldKls1KOShOWxZNbpZyrbgO1kNArRAfwW3I"
# }

# requests.patch("https://api.datawrapper.de/v3/charts", json=payload, headers=headers)

# records.to_csv("assets/data/graphics.csv")








# for state in raw["State"].unique():
#     print(state)
# #     print(state)
#     state_data = raw.loc[raw["State"] == state, ["YEAR", "RATE"]].sort_values("YEAR").loc[raw["YEAR"] != 2005, :].set_index("YEAR")
#     print(state_data)
#     linechart = dwmaps.Chart(copy_id="s8lzT").data(state_data).head(f"Gun violence in {state}").publish()
#     record = pd.DataFrame({"state": [state], "chart_id": [linechart.CHART_ID]})
#     state_graphics.append(record)
    
    
    
    
    
    
# for id in charts["chart_id"].unique():
#     linechart = dwmaps.Chart(id).publish()
    
    
    
    
    
    
