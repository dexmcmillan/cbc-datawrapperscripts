import geopandas
import pandas as pd
import dwmaps

CHART_ID = "83uUC"

data = pd.read_xml("https://www.nhc.noaa.gov/nhc_ep1.xml", xpath="/rss/channel/item[1]/nhc:Cyclone", namespaces={"nhc":"https://www.nhc.noaa.gov"})
data["latitude"] = pd.Series(data.at[0, "center"].split(",")[0].strip()).astype(float)
data["longitude"] = pd.Series(data.at[0, "center"].split(",")[1].strip()).astype(float)

print(data)

windspeed = data.at[0, "wind"].replace(" mph", "")
windspeed = int(int(windspeed) * 1.60934)

date = data.at[0,"datetime"]

data = data[["latitude", "longitude"]]
data["type"] = "point"
data["icon"] = "circle-sm"
data["markerColor"] = "#333333"
data["title"] = ""
data["scale"] = 1.7
data["tooltip"] = f"The eye of Hurricane Agatha is currently here."
data["fill"] = "#C42127"


path1 = geopandas.read_file("https://www.nhc.noaa.gov/gis/forecast/archive/ep012022_5day_latest.zip", layer="ep012022-011_5day_lin")
path2 = geopandas.read_file("https://www.nhc.noaa.gov/gis/forecast/archive/ep012022_5day_latest.zip", layer="ep012022-011_5day_pgn")

path = pd.concat([path1, path2])

path["fill"] = "#C42127"
path["fill-opacity"] = [0.0, 0.2]
path["stroke"] = ["black", "#C42127"]
path["type"] = "area"
path["icon"] = "area"
path["geometry"] = path["geometry"].simplify(0.01)

path = pd.concat([path, data])

path = path[["markerColor", "fill", "fill-opacity", "stroke", "type", "icon", "latitude", "longitude", "geometry", "title", "tooltip", "scale"]]
path["latitude"] = path["latitude"].fillna("")
path["longitude"] = path["longitude"].fillna("")

print(path)

hurricane_map = (dwmaps.Map(CHART_ID)
                 .data(path)
                 .head(f"Tracking Hurricane Agatha")
                 .deck(f"Windspeed is currently measured at <b>{windspeed} km/h</b>. The shaded region shows a range of probable paths for the storm over the next 5 days.")
                 .footer(source="U.S. National Hurricane Center")
                 .publish()
                 )