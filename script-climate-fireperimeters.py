import requests
import geopandas
import pandas as pd
import json
import datawrappergraphics
import logging
import datetime as dt

# Live chart ID: Os1m6
MAP_ID = "80lJz"
CHART_ID = "0NmJU"

# Make HTTP request for the data and put into a geopandas dataframe.
raw = geopandas.read_file("/vsicurl/https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/", driver="shapefile", layer="perimeters")
# data = geopandas.read_file(json.dumps(r.json()))
raw["type"] = "area"
raw["LASTDATE"] = pd.to_datetime(raw["LASTDATE"])
raw.loc[raw["LASTDATE"] == dt.datetime.today(), "active"] = True
raw["active"] = raw["active"].fillna(False)
print(raw)

datawrappergraphics.Chart(MAP_ID).data(raw).head(f"There are {len(raw)} fires burning in Canada right now, covering {'{:,}'.format(raw['AREA'].sum())} hectares of land.")

# # Change colour of the marker based on the fire status.
# data["markerColor"] = data["FIRE_STATUS"].replace({"Under Control": "#436170", "New": "#F8C325", "Out of Control": "#c42127", "Being Held": "#000000"})

# # Define type as point and icon as fire.
# data["type"] = "point"
# data["icon"] = "fire"

# # Calculate scale of each item based on the side of the fire.
# avg = data["CURRENT_SIZE"].min()
# std = data["CURRENT_SIZE"].std()
# data["scale"] = ((data["CURRENT_SIZE"] - avg) / (std)) + 1

# # This line caps scale at a certain value.
# data["scale"] = data["scale"].apply(lambda x: 2.2 if x > 2.2 else x)

# # Build tooltip from description and status.
# data["tooltip"] = "<big>Fire at " + data['GEOGRAPHIC_DESCRIPTION'] + "</big><br><b>Status</b>: " + data['FIRE_STATUS'] + "</span><br><b>Started by</b>: " + data["FIRE_CAUSE"] + "<br><b>Estimated size</b>: " + data["CURRENT_SIZE"].astype(str) + " hectares"
# data = data.sort_values("scale")

# map = (datawrappergraphics.Map(chart_id=MAP_ID)
#             .data(raw)
#             .head(f"TEST: Floods in Canada")
#             .publish()
#             )