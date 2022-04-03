import pandas as pd
import requests
import json
from ast import literal_eval

from ukraineshape import ukraine

## The ID of the Ukraine map Datawrapper.
CHART_ID = "sM21M"

## Import sheet data.
raw = pd.read_csv("https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/export?format=csv&gid=0", encoding="utf-8").dropna(how="all", axis=1)

## Rename columns from the spreadsheet.
raw.columns = ["title", "tooltip", "source", "hide_title", "visible", "coordinates", "anchor"]

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

data["tooltip"] = '{"text": "<b>' + data["title"] + "</b><br>" + data["tooltip"].str.strip().str.replace("\"", "'") + '"}'
data["tooltip"] = data["tooltip"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["markerColor"] = "#c42127"
data["coordinates"] = data["coordinates"].apply(literal_eval)
data["type"] = "point"
data["id"] = range(0,len(data))
data["icon"] = "{'id': 'circle-sm','path': 'M1000 350a500 500 0 0 0-500-500 500 500 0 0 0-500 500 500 500 0 0 0 500 500 500 500 0 0 0 500-500z','horiz-adv-x': 1000,'scale': 0.42,'height': 700,'width': 1000}"
data["icon"] = data["icon"].apply(literal_eval)
data["scale"] = 1

## Convert only the columns we need to JSON.
data_json = (data
             .loc[:, ["title", "type", "coordinates", "markerColor", "tooltip", "icon", "scale", "id", "visible", "anchor"]]
             .to_json(orient='records', index=True)
             )
payload = json.loads(data_json)

## Append the ukraine shape to our data.
payload.append(ukraine)

## Package into the right format for Datawrapper API.
payload = {"markers": payload}

## Define headers for chart update API.
headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": "Bearer f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF",
}

## Update chart.
response = requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data", headers=headers, data=json.dumps(payload))

print(response)