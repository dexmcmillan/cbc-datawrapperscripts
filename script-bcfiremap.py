import requests
import geopandas
import pandas as pd
import json
import dwmaps

# Live chart ID: Os1m6
CHART_ID = "Os1m6"

# Make HTTP request for the data and put into a geopandas dataframe.
r = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_ActiveFires_PublicView/FeatureServer/0/query?f=json&where=FIRE_STATUS%20%3C%3E%20%27Out%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=FIRE_YEAR,IGNITION_DATE,FIRE_STATUS,FIRE_CAUSE,FIRE_CENTRE,ZONE,FIRE_ID,FIRE_TYPE,GEOGRAPHIC_DESCRIPTION,LATITUDE,LONGITUDE,CURRENT_SIZE,FIRE_OF_NOTE_ID,FIRE_OF_NOTE_NAME,FIRE_OF_NOTE_URL,FEATURE_CODE,OBJECTID&orderByFields=OBJECTID%20ASC&outSR=102100")
data = geopandas.read_file(json.dumps(r.json()))

# Define opacity for the markers.
data["opacity"] = 0.5

# Change colour of the marker based on the fire status.
data["markerColor"] = data["FIRE_STATUS"].replace({"Under Control": "#436170", "New": "#F8C325", "Out of Control": "#c42127", "Being Held": "#000000"})

# Define type as point and icon as fire.
data["type"] = "point"
data["icon"] = "fire"

# Calculate scale of each item based on the side of the fire.
avg = data["CURRENT_SIZE"].min()
std = data["CURRENT_SIZE"].std()
data["scale"] = ((data["CURRENT_SIZE"] - avg) / (std)) + 1

# This line caps scale at a certain value.
data["scale"] = data["scale"].apply(lambda x: 2.2 if x > 2.2 else x)

# Build tooltip from description and status.
data["tooltip"] = "<big>Fire at " + data['GEOGRAPHIC_DESCRIPTION'] + "</big><br><b>Status</b>: " + data['FIRE_STATUS'] + "</span><br><b>Started by</b>: " + data["FIRE_CAUSE"] + "<br><b>Estimated size</b>: " + data["CURRENT_SIZE"].astype(str) + " hectares"
data = data.sort_values("scale")

map = (dwmaps.Map(chart_id=CHART_ID)
            .data(data)
            .head(f"There are <b>{len(data)} wildfires</b> burning across B.C.")
            .deck(f"As of today, {round(len(data[data['FIRE_STATUS'] == 'Under Control'])/len(data)*100, 1)}% are listed as under control. Size of markers approximately represents the size of the fire.")
            .footer(source="B.C. Wildfire Centre")
            .publish()
            )