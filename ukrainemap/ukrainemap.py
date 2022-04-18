import pandas as pd
import requests
import json
import datetime as dt
import os

try:
    from config import DW_AUTH_TOKEN
except ModuleNotFoundError:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']

## The ID of the Ukraine map Datawrapper. (LIVE CHART ID: wQIM1. TEST CHART ID: sM21M)
CHART_ID = "wQIM1"

## Import sheet data.
raw = (pd
       .read_csv("https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/export?format=csv&gid=0", encoding="utf-8")
       .dropna(how="all", axis=1)
       )

## Rename columns from the spreadsheet.
raw.columns = ["title", "tooltip", "source", "hide_title", "visibility", "coordinates", "anchor", "icon"]

marker_properties = [
    "title",
    "type",
    "coordinates",
    "markerColor",
    "tooltip",
    "icon",
    "scale",
    "id",
    "visibility",
    "visible",
    "anchor",
    "text",
    "offsetX",
    "offsetY"
]

## Clean data.
data = (raw
        .dropna(how="all")
        .set_index("title")
        .drop("LOCATION")
        .reset_index()
        )

data["visible"] = data["visibility"].astype(str).str.lower().apply(lambda x: json.loads(x, strict=False))

data["source"] = data["source"].fillna("")

data["visibility"] = (data["visible"].apply(lambda x: { "mobile": x, "desktop": x }))

data["anchor"] = data["anchor"].str.lower()

data["tooltip"] = data["tooltip"].str.strip().str.replace("\"", '\\"')

data["tooltip"] = '{"text": "<b>' + data["title"] + '</b><br>' + data["tooltip"] + ' <i>(Source: ' + data["source"].fillna("").str.strip().str.replace("\"", "'") + ')</i>"}'

data["tooltip"] = data["tooltip"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["markerColor"] = "#c42127"

data["coordinates"] = data["coordinates"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["type"] = "point"

data["id"] = ['m'+str(x) for x in range(2, len(data) + 2)]

data["icon"] = '{"id": "' + data["icon"] + '","path": "M1000 350a500 500 0 0 0-500-500 500 500 0 0 0-500 500 500 500 0 0 0 500 500 500 500 0 0 0 500-500z","horiz-adv-x": 1000,"scale": 0.42,"height": 700,"width": 1000}'
data["icon"] = data["icon"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["scale"] = 1.2

data["text"] = [{
    "bold": False,
    "color": "#333333",
    "fontSize": 14,
    "halo": "#f2f3f0",
    "italic": False,
    "space": False,
    "uppercase": False
}] * len(data)

data["offsetX"] = 0
data["offsetY"] = 0

## Convert only the columns we need to JSON.
data_json = (data
             .loc[:, marker_properties]
             .to_json(orient='records', index=True)
             )
payload = json.loads(data_json)

## Append the shapes for Crimea, Ukraine etc to our data.
with open("ukrainemap/shapes.json", 'r') as jsonFile:
    jsonObject = json.load(jsonFile)
    for shape in jsonObject:
        payload.append(shape)
    jsonFile.close()


## Package into the right format for Datawrapper API.
payload = {"markers": payload}

## Define headers for chart update API.
headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": f"Bearer {DW_AUTH_TOKEN}",
}

## Update chart.
response = requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data", headers=headers, data=json.dumps(payload))

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DW_AUTH_TOKEN}",
}

## If this is running via github actions, you'll want to subtract 4 hours from the day variable.

today = dt.datetime.today()
day = (today).strftime('%B %d, %Y')
time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."

source_list = set(raw.loc[raw["visibility"] == "TRUE","source"].to_list())
source_list_clean = []
for entry in source_list:
    try:
        word = entry.split(", ")
        source_list_clean.append(word)
    except:
        pass

source_list_clean = [item for sublist in source_list_clean for item in sublist]
source_list_clean = [x for x in source_list_clean if x]
source_list_clean = set(source_list_clean)


source_string = ", ".join(source_list_clean)
print(source_string)

metadata_update = {"metadata": {
    "annotate": {
        "notes": f"Last updated on {day} at {time} EST.".replace(" 0", " ")
    },
    "describe": {
        "source-name": source_string + "."
    }
}
}

requests.request("PATCH", f"https://api.datawrapper.de/v3/charts/{CHART_ID}", json=metadata_update, headers=headers)
requests.request("POST", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/publish", headers=headers)