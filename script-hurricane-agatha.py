import geopandas
import pandas as pd
import dwmaps
import pytz
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen



                

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

filename = "https://www.nhc.noaa.gov/gis/forecast/archive/ep012022_5day_latest.zip"

resp = urlopen(filename)
files = ZipFile(BytesIO(resp.read())).namelist()
files = pd.Series(files)

lines_file_name = files[files.str.contains("5day_lin.shp$")].to_list()[0].replace(".shp", "")
shape_file_name = files[files.str.contains("5day_pgn.shp$")].to_list()[0].replace(".shp", "")
points_file_name = files[files.str.contains("5day_pts.shp$")].to_list()[0].replace(".shp", "")

path1 = geopandas.read_file(filename, layer=lines_file_name)
path2 = geopandas.read_file(filename, layer=shape_file_name)
path3 = geopandas.read_file(filename, layer=points_file_name)

path3["longitude"] = path3["geometry"].x.astype(float)
path3["latitude"] = path3["geometry"].y.astype(float)
path3 = path3.drop(columns=["geometry"])

eastern = pytz.timezone('US/Eastern')
path3["DATELBL"] = pd.to_datetime(path3["DATELBL"]).apply(lambda x: x.tz_localize("America/Chicago"))
path3["DATELBL"] = path3["DATELBL"].dt.tz_convert('US/Eastern')

path3.to_clipboard()

path3["type"] = "point"
path3["icon"] = "circle"
path3["markerColor"] = "#333333"
path3["title"] = path3['DATELBL'].dt.strftime("%b %e") + "<br>" + path3['DATELBL'].dt.strftime("%I:%M %p")
path3["title"] = path3["title"].str.replace("<br>0", "<br>")
path3["scale"] = 1.1

path3.loc[path3["DVLBL"] == "D", "storm_type"] = "Depression"
path3.loc[path3["DVLBL"] == "H", "storm_type"] = "Hurricane"
path3.loc[path3["DVLBL"] == "S", "storm_type"] = "Storm"

path3["tooltip"] = "On " + path3['DATELBL'].dt.strftime("%b %e") + " at " + path3['DATELBL'].dt.strftime("%I:%M %p").str.replace("$0", "", regex=True) + " EST, the storm is projected to be classified as a " + path3["storm_type"].str.lower() + "."
path3["tooltip"] = path3["tooltip"].str.replace(" 0", " ")
path3["fill"] = "#C42127"
path3["markerSymbol"] = path3["DVLBL"]

path1["type"] = "area"
path1["icon"] = "area"
path1["fill"] = "#C42127"
path1["stroke"] = "#000000"
path1["markerColor"] = "#C42127"
path1["fill-opacity"] = 0.0
    
path2["icon"] = "area"
path2["type"] = "area"
path2["fill"] = "#6a3d99"
path2["stroke"] = "#6a3d99"
path2["markerColor"] = "#6a3d99"
path2["fill-opacity"] = 0.2

path = pd.concat([path1, path2, path3, data])

path = path[["markerColor", "fill", "fill-opacity", "stroke", "type", "icon", "latitude", "longitude", "geometry", "title", "tooltip", "scale", "markerSymbol"]]
path["latitude"] = path["latitude"].fillna("")
path["longitude"] = path["longitude"].fillna("")

print(path)

hurricane_map = (dwmaps.Map(CHART_ID)
                 .data(path)
                 .head(f"Tracking Hurricane Agatha")
                 .deck(f"Windspeed is currently measured at <b>{windspeed} km/h</b>. The shaded region shows a range of probable paths for the storm over the next five days.")
                 .footer(source="U.S. National Hurricane Center")
                 .publish()
                 )