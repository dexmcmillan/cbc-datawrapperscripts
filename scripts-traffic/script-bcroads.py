import pandas as pd
import datawrappergraphics

chart_id = "wmdZl"

data = pd.read_json("https://drivebc.ca/data/events.json")
data = data[[0,1,2,3,4,9]]
data.columns = ["type1", "latitude", "longitude", "location1", "location2", "tooltip"]

data["icon"] = "circle-sm"

data["tooltip"] = "<b>" + data["location1"] + " - " + data["location2"] + "</b><br>" + data["tooltip"]

incidents = data[data["type1"] == "INCIDENT"]

map = datawrappergraphics.Map(chart_id).data(incidents).head("A test map of BC provincial traffic conditions")