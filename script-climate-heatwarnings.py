import geopandas
import datawrappergraphics

raw = geopandas.read_file("https://geo.weather.gc.ca/geomet?service=wfs&version=2.0.0&request=GetFeature&typeNames=ALERTS&outputFormat=GeoJSON", driver="geojson")
data = raw[raw["alert_type"] == "warning"]
data["title"] = data["descrip_en"]
data["fill-opacity"] = 0.8

(datawrappergraphics.Map("1XHZ5")
 .data(data, append="./assets/shapes/shapes-heatwarnings.json")
 .head(f"There are {int(len(data))} heat warnings in effect across Canada right now")
 .footer(source="Environment and Climate Change Canada", timestamp=True, byline="Wendy Martinez, Dexter McMillan")
 .publish()
 )