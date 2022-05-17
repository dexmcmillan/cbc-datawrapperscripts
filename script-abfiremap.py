import requests
import geopandas
import pandas as pd
import json
import dwmaps

CHART_ID = "L45df"

r = requests.get("https://services.arcgis.com/Eb8P5h4CJk8utIBz/ArcGIS/rest/services/Active_Wildfire_Locations/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=standard&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=")

data = geopandas.read_file(json.dumps(r.json()))

print(data.columns)

data["opacity"] = 0.5
data = data.drop(columns="ID")
data['id'] = range(0, len(data))
data["id"] = data['id'].apply(lambda x: f"m{x}")
data["title"] = ""
data["type"] = "points"
data["fill"] = "black"
data["stroke"] = "black"

data["icon"] = "fire"

data["markerColor"] = data["FIRE_STATUS"].replace({"Under Control": "#436170", "New": "#F8C325"})

data["type"] = "point"

avg = data["AREA_ESTIMATE"].min()
std = data["AREA_ESTIMATE"].std()

data["scale"] = ((data["AREA_ESTIMATE"] - avg) / (std)) + 1
data["scale"] = data["scale"].apply(lambda x: 2.2 if x > 2.2 else x)

data["tooltip"] = "<big>" + data['LABEL'] + "</big><br><b>Status</b>: " + data['FIRE_STATUS'] + "</span>"


print(data.columns)
chart = dwmaps.DatawrapperMaps(chart_id=CHART_ID)
dw = (chart
      .upload(data)
      .head(f"There are <b>{len(data)} wildfires</b> burning across Alberta")
      .deck(f"As of today, {round(len(data[data['FIRE_STATUS'] == 'Under Control'])/len(data)*100, 1)}% are listed as under control.", "Government of Alberta")
      .timestamp()
      .publish()
      )