import requests
import geopandas
import pandas as pd
import json
import datawrappergraphics
import logging

map_id = "ln2qq"

raw = geopandas.read_file("/vsicurl/https://cwfis.cfs.nrcan.gc.ca/downloads/hotspots", layer="progression", driver="shapefile")
# raw["type"] = "area"
# raw["title"] = raw["UID"]


# (datawrappergraphics
#  .Map(map_id)
#  .data(raw)
#  .head(f"TEST: Wildfire perimeter map")
#  .publish()
# )

print(raw)


ids = raw.value_counts()

print(ids)