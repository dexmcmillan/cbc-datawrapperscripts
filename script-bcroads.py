import pandas as pd
import dwmaps

data = pd.read_json("https://drivebc.ca/data/events.json")
data = data[[0,1,2,3,4,9]]
data.columns = ["type1", "latitude", "longitude", "location1", "location2", "tooltip"]

data["icon"] = "circle-sm"
data["markerColor"] = "#c42127"
data["type"] = "point"

data["tooltip"] = "<b>" + data["location1"] + " - " + data["location2"] + "</b><br>" + data["tooltip"]

incidents = data[data["type1"] == "INCIDENT"]

map = dwmaps.Map("wmdZl").data(incidents).head("A test map of BC provincial traffic conditions")