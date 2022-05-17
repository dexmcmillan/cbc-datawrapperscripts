import requests
import geopandas
import pandas as pd
import json
import dwmaps

CHART_ID = "Os1m6"

r = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_ActiveFires_PublicView/FeatureServer/0/query?f=json&where=FIRE_STATUS%20%3C%3E%20%27Out%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=FIRE_YEAR,IGNITION_DATE,FIRE_STATUS,FIRE_CAUSE,FIRE_CENTRE,ZONE,FIRE_ID,FIRE_TYPE,GEOGRAPHIC_DESCRIPTION,LATITUDE,LONGITUDE,CURRENT_SIZE,FIRE_OF_NOTE_ID,FIRE_OF_NOTE_NAME,FIRE_OF_NOTE_URL,FEATURE_CODE,OBJECTID&orderByFields=OBJECTID%20ASC&outSR=102100")

data = geopandas.read_file(json.dumps(r.json()))

print(data)

data["opacity"] = 0.5
data['id'] = range(0, len(data))
data["id"] = data['id'].apply(lambda x: f"m{x}")
data["title"] = ""
data["type"] = "points"
data["fill"] = "black"
data["stroke"] = "black"

data["icon"] = "fire"

data["markerColor"] = data["FIRE_STATUS"].replace({"Under Control": "#436170", "New": "#F8C325"})

data["type"] = "point"

avg = data["CURRENT_SIZE"].min()
std = data["CURRENT_SIZE"].std()

data["scale"] = ((data["CURRENT_SIZE"] - avg) / (std)) + 1

data["tooltip"] = "<big>Fire at " + data['GEOGRAPHIC_DESCRIPTION'] + "</big><br><b>Status</b>: " + data['FIRE_STATUS'] + "</span><br><b>Started by</b>: " + data["FIRE_CAUSE"] + "<br><b>Estimated size</b>: " + data["CURRENT_SIZE"].astype(str) + " hectares"



chart = dwmaps.DatawrapperMaps(chart_id=CHART_ID)
dw = (chart
      .upload(data)
      .head(f"There are <b>{len(data)} wildfires</b> burning across B.C.")
      .deck(f"As of today, {round(len(data[data['FIRE_STATUS'] == 'Under Control'])/len(data)*100, 1)}% are listed as under control.", "B.C. Wildfire Centre")
      .timestamp()
      )