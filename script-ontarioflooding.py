import pandas as pd
from datawrappergraphics.Map import Map

CHART_ID = "Zuvdy"

raw = pd.read_json("https://511on.ca/api/v2/get/event")

data = raw[raw["EventType"] == "closures"]
data = data[["Description", "LanesAffected", "Latitude", "Longitude"]]
data.columns = ["tooltip", "LanesAffected", "latitude", "longitude"]

data["color"] = "#C42127"
data["icon"] = "attention"
data["title"] = ""
data["scale"] = 1.2
data["type"] = "point"
data["markerColor"] = "#C42127"

roadmap = (Map(CHART_ID)
            .data(data)
            .head(f"Northern Ontario road closures due to flooding")
            .deck(f"There are currently <b>{len(data)} road closures</b>, according to Ontario 511. Tap or hover over a red triangle to read more about the closure.")
            .footer(source="Ontario 511")
            .publish()
            )