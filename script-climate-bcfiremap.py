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

data["stroke"] = False

# markers = datawrappergraphics.Map(chart_id=CHART_ID).get_markers()[0:2]

# with open('./assets/shapes/shapes-bcfiremap.json', 'w', encoding='utf-8') as f:
#     json.dump(markers, f)



map = (datawrappergraphics.Map(chart_id=CHART_ID)
            .data(data, append="./assets/shapes/shapes-bcfiremap.json")
            .footer(source="B.C. Wildfire Centre")
            .publish()
            )