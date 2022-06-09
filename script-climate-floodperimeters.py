from email.contentmanager import raw_data_manager
import requests
import geopandas
import pandas as pd
import json
import datawrappergraphics
import logging

# Live chart ID: Os1m6
CHART_ID = "80lJz"

# Make HTTP request for the data and put into a geopandas dataframe.
raw = geopandas.read_file("https://maps-cartes.services.geo.ca/egs_sgu/rest/services/Flood_Inondation/EGS_Flood_Product_Active_en/MapServer/1/query?where=1%3D1&text=fire&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson")
# data = geopandas.read_file(json.dumps(r.json()))
raw["type"] = "area"
print(raw)

raw["geometry"] = raw["geometry"].simplify(0.1)

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

map = (datawrappergraphics.Map(chart_id=CHART_ID)
            .data(raw)
            .head(f"TEST: Floods in Canada")
            .publish()
            )