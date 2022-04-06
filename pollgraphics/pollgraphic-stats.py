import pandas as pd
import requests
import os
from datawrapper import Datawrapper

# This code runs differently depending on whether the script is running on a local machine or via Github actions.

try:
    from config import DW_AUTH_TOKEN
except ModuleNotFoundError:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
    
# Read in data from the poll tracker API into a pandas dataframe.

raw = requests.get("https://canopy.cbc.ca/live/poll-tracker/v4/CAN").json()['data']["stats"]

# Reshape the data a little bit to prepare it for the datawrapper.
regions = raw[0]["rows"].keys()
parties = raw[0]["rows"]["Canada"].keys()

data = []

for region in regions:
    for party in parties:
        df = (pd
                .json_normalize(raw, record_path=["rows", region, party, "share"], meta=["datetime"])
        )
        df["Party"] = party
        df["Region"] = region
        df["Type"] = ["min", "low", "med", "high", "max"] * int((len(df.index)/5))
        data.append(df)

data = pd.concat(data)

export = data[(data["Type"] == "med") & (data["Region"] == "Ontario")].pivot(index="datetime", columns="Party", values=0)

for col, values in export.iteritems():
    export[col + "_rolling"] = export[col].rolling(7).mean()
    
export = export.dropna().reset_index()

# Use the Datawrapper python module to update the data in the chart.
dw = Datawrapper(access_token=DW_AUTH_TOKEN)

# Add above data to over time polling line chart.
dw.add_data(chart_id="VxY9x", data=export)

# Most recent polling data chart.
recent = export.sort_values("datetime", ascending=False).iloc[0:2, 0:8].set_index("datetime").transpose().reset_index()

dw.add_data(chart_id="9ya4P", data=recent)