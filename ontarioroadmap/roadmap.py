import pandas as pd
import json
import os
import requests
import datetime as dt

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']

## The ID of the Ukraine map Datawrapper.
CHART_ID = "WG4XF"

raw = pd.read_json("https://511on.ca/api/v2/get/event")

data = raw[raw["EventType"] == "closures"]

data = data[["Description", "LanesAffected", "Latitude", "Longitude"]]
data.columns = ["tooltip", "LanesAffected", "lat", "lng"]
data["color"] = "#C42127"

data["icon"] = '{"id": "attention","path": "M957-24q10-16 0-34-10-16-30-16l-892 0q-18 0-28 16-13 18-2 34l446 782q8 18 30 18t30-18z m-420 50l0 100-110 0 0-100 110 0z m0 174l0 300-110 0 0-300 110 0z","horiz-adv-x": 962,"height": 702,"width": 961.3333333333333}'
data["icon"] = data["icon"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

data["title"] = ""

data["tooltip"] = '{"text": "' + data["tooltip"] + '"}'
data["tooltip"] = data["tooltip"].astype(str).apply(lambda x: json.loads(x.strip(), strict=False))

print(data)

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

data["type"] = "point"

data["id"] = ['m'+str(x) for x in range(2, len(data) + 2)]

data["markerColor"] = "#C42127"

data["visible"] = True

data["visibility"] = (data["visible"].apply(lambda x: { "mobile": x, "desktop": x }))

data["anchor"] = "top-center"

data["coordinates"] = "[" + data["lng"].astype(str) + "," + data["lat"].astype(str) + "]"
data["coordinates"] = data["coordinates"].apply(lambda x: json.loads(x))


## Convert only the columns we need to JSON.
data_json = (data
             .loc[:, marker_properties]
             .to_json(orient='records', index=True)
             )
payload = json.loads(data_json)

## Append the shapes for Crimea, Ukraine etc to our data.
with open("ontarioroadmap/shapes.json", 'r') as jsonFile:
    jsonObject = json.load(jsonFile)
    for shape in jsonObject:
        payload.append(shape)
    jsonFile.close()

## Package into the right format for Datawrapper API.
payload = {"markers": payload}

print(payload)

## Define headers for chart update API.
headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": f"Bearer {DW_AUTH_TOKEN}",
}

## Update chart.
response = requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data", headers=headers, data=json.dumps(payload))

print(response)

# Define new headers for Metadata update.

headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DW_AUTH_TOKEN}",
}

today = dt.datetime.today() - dt.timedelta(hours=4)
day = today.strftime('%B %d, %Y')
time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."

metadata_update = {"metadata": {
    "annotate": {
        "notes": f"Last updated on {day} at {time} EST.".replace(" 0", " ")
    }
}
}

## Publish chart
update = requests.request("PATCH", f"https://api.datawrapper.de/v3/charts/{CHART_ID}", json=metadata_update, headers=headers)
print(update.text)
requests.request("POST", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/publish", headers=headers)