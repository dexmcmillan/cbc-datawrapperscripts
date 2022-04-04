import pandas as pd
import requests
import json
import datetime as dt
import os

try:
    from config import DW_AUTH_TOKEN
except ModuleNotFoundError:
    # Error handling
    pass

## The ID of the Ukraine map Datawrapper.
CHART_ID = "sM21M"

if 'DW_AUTH_TOKEN' in os.environ:
    AUTH_KEY = os.environ['DW_AUTH_TOKEN']
else:
    AUTH_KEY = DW_AUTH_TOKEN


## Import sheet data.
raw = pd.read_csv("https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/export?format=csv&gid=0", encoding="utf-8").dropna(how="all", axis=1)

## Rename columns from the spreadsheet.
raw.columns = ["title", "tooltip", "source", "hide_title", "visible", "coordinates", "anchor", "icon"]

## Clean data.
data = (raw
        .dropna(how="all")
        .set_index("title")
        .drop("LOCATION")
        .reset_index()
        )

data["visible"] = (data["visible"]
                   .astype(str)
                   .str.lower()
                   .apply(lambda x: json.loads(x, strict=False))
                    )

data["anchor"] = data["anchor"].str.lower()

data["tooltip"] = data["tooltip"].str.strip().str.replace("\"", '\\"')
data["tooltip"] = '{"text": "<b>' + data["title"] + '</b><br>' + data["tooltip"] + ' <i>(Source: ' + data["source"].fillna("").str.strip().str.replace("\"", "'") + ')</i>"}'

data["tooltip"] = data["tooltip"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["markerColor"] = "#c42127"

data["coordinates"] = data["coordinates"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["type"] = "point"

data["id"] = range(0,len(data))

data["icon"] = '{"id": "' + data["icon"] + '","path": "M1000 350a500 500 0 0 0-500-500 500 500 0 0 0-500 500 500 500 0 0 0 500 500 500 500 0 0 0 500-500z","horiz-adv-x": 1000,"scale": 0.42,"height": 700,"width": 1000}'
data["icon"] = data["icon"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["scale"] = 1.3

## Convert only the columns we need to JSON.
data_json = (data
             .loc[:, ["title", "type", "coordinates", "markerColor", "tooltip", "icon", "scale", "id", "visible", "anchor"]]
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
    "Authorization": f"Bearer {AUTH_KEY}",
}

## Update chart.
response = requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data", headers=headers, data=json.dumps(payload))

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_KEY}",
}

today = dt.datetime.today()
day = (today - dt.timedelta(hours=4)).strftime('%B %d, %Y')
time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."

metadata_update = {"metadata": {
    "annotate": {
        "notes": f"Last updated on {day} at {time} EST.".replace(" 0", " ")
    }
}
}

response = requests.request("PATCH", f"https://api.datawrapper.de/v3/charts/{CHART_ID}", json=metadata_update, headers=headers)

requests.request("POST", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/publish", headers=headers)