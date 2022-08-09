import requests
import geopandas
import pandas as pd
import json
import datawrappergraphics

# Live chart ID: Os1m6
CHART_ID = "FAPp3"

# Make HTTP request for the data and put into a geopandas dataframe.
data = geopandas.read_file("/vsicurl/https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots/perimeters.shp")

data = data.to_crs("EPSG:4326")

data["stroke"] = "#C42127"
data["stroke-width"] = 2
data["fill-opacity"] = 0.3
data["fill"] = "#C42127"
data["title"] = data["UID"]

# markers1 = [datawrappergraphics.Map(chart_id=CHART_ID).get_markers()[0]]
# markers2 = datawrappergraphics.Map(chart_id=CHART_ID).get_markers()[-2:]

# markers = [x for n in (markers1, markers2) for x in n]

# with open('./assets/shapes/shapes-nlfiremap.json', 'w', encoding='utf-8') as f:
#     json.dump(markers, f)


# data = data[data["UID"].isin([8709641, 8709640])]


highway = geopandas.read_file("./assets/shapes/highway.geojson")
highway["fill"] = False
highway["stroke"] = "#000000"
highway["stroke-width"] = 2

data = data.append(highway)

print(data)

map = (datawrappergraphics.Map(chart_id=CHART_ID)
            .data(data, append="./assets/shapes/shapes-nlfiremap.json")
            .footer(source="Natural Resources Canada")
            .publish()
            )