import requests
import geopandas
import pandas as pd
import json
import datawrappergraphics

# Live chart ID: Os1m6
CHART_ID = "Os1m6"

# Make HTTP request for the data and put into a geopandas dataframe.
r = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BCWS_FirePerimeters_PublicView/FeatureServer/0/query?f=json&where=1=1")
data = geopandas.read_file(json.dumps(r.json()))
data = data.to_crs("EPSG:4326")

data["stroke"] = "#C42127"
data["stroke-width"] = 2
data["fill"] = False

# evac = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services/Evacuation_Orders_and_Alerts/FeatureServer/0/query?where=ORDER_ALERT_STATUS+%3C%3E+%27All+Clear%27+AND+EVENT_TYPE+%3D+%27Fire%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=OBJECTID,EVENT_NAME,ORDER_ALERT_STATUS&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=")
# evac = geopandas.read_file(json.dumps(evac.json()))

# evac.loc[evac["ORDER_ALERT_STATUS"] == "Alert", "fill"] = "#F8C325"
# evac.loc[evac["ORDER_ALERT_STATUS"] == "Order", "fill"] = "#C42127"
# evac["stroke"] = False
# evac["title"] = evac["EVENT_NAME"]
# evac = evac[evac["title"] == "Keremeos Creek Wildfire"]

# data = data.append(evac)

# markers1 = datawrappergraphics.Map(chart_id=CHART_ID).get_markers()[0:2]
# markers2 = datawrappergraphics.Map(chart_id=CHART_ID).get_markers()[-5:]

# markers = [x for n in (markers1, markers2) for x in n]


# with open('./assets/shapes/shapes-bcfiremap.json', 'w', encoding='utf-8') as f:
#     json.dump(markers, f)

# data["fill"] = data["fill"].fillna("#C42127")

map = (datawrappergraphics.Map(chart_id=CHART_ID)
            .data(data, append="./assets/shapes/shapes-bcfiremap.json")
            .footer(source="B.C. Wildfire Centre")
            .publish()
            )