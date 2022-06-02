import geopandas
import pandas as pd
import dwmaps
import pytz
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


def get_shapefile(filename, layer):
    resp = urlopen(filename)
    files = ZipFile(BytesIO(resp.read())).namelist()
    files = pd.Series(files)

    total_path_file_name = files[files.str.contains(layer)].to_list()[0].replace(".shp", "")
    return geopandas.read_file(filename, layer=total_path_file_name)


CHART_ID = "nSHo0"

best_track_zip = "https://www.nhc.noaa.gov/gis/best_track/ep012022_best_track.zip"
total_path = get_shapefile(best_track_zip, "pts.shp$")

total_path_line = get_shapefile(best_track_zip, "lin.shp$")

total_path = total_path[total_path["STORMNAME"] == "AGATHA"]
total_path = total_path.rename(columns={"LAT": "latitude", "LON": "longitude"})

total_path["longitude"] = total_path["geometry"].x.astype(float)
total_path["latitude"] = total_path["geometry"].y.astype(float)
total_path = total_path.drop(columns=["geometry"])

total_path["type"] = "point"
total_path["icon"] = "circle"
total_path["markerColor"] = "#333333"
total_path["scale"] = 1.1
total_path["tooltip"] = ""
total_path["title"] = ""

total_path.loc[total_path["STORMTYPE"] == "D", "storm_type"] = "Depression"
total_path.loc[total_path["STORMTYPE"] == "H", "storm_type"] = "Hurricane"
total_path.loc[total_path["STORMTYPE"] == "S", "storm_type"] = "Storm"

total_path["fill"] = "#C42127"
total_path["markerSymbol"] = total_path["STORMTYPE"]

data = pd.read_xml("https://www.nhc.noaa.gov/nhc_ep1.xml", xpath="/rss/channel/item[1]/nhc:Cyclone", namespaces={"nhc":"https://www.nhc.noaa.gov"})
data["latitude"] = pd.Series(data.at[0, "center"].split(",")[0].strip()).astype(float)
data["longitude"] = pd.Series(data.at[0, "center"].split(",")[1].strip()).astype(float)

windspeed = data.at[0, "wind"].replace(" mph", "")
windspeed = int(int(windspeed) * 1.60934)
name = data.at[0, "type"] + " " + data.at[0, "name"]

date = data.at[0,"datetime"]

data = data[["latitude", "longitude"]]
data["type"] = "point"
data["icon"] = "circle-sm"
data["markerColor"] = "#333333"
data["title"] = ""
data["scale"] = 1.7
data["tooltip"] = f"The eye of Hurricane Agatha is currently here."
data["fill"] = "#C42127"

five_day_latest_filename = "https://www.nhc.noaa.gov/gis/forecast/archive/ep012022_5day_latest.zip"

centre_line = get_shapefile(five_day_latest_filename, "5day_lin.shp$")
probable_path = get_shapefile(five_day_latest_filename, "5day_pgn.shp$")
points = get_shapefile(five_day_latest_filename, "5day_pts.shp$")

points["longitude"] = points["geometry"].x.astype(float)
points["latitude"] = points["geometry"].y.astype(float)
points = points.drop(columns=["geometry"])

eastern = pytz.timezone('US/Eastern')
points["DATELBL"] = pd.to_datetime(points["DATELBL"]).apply(lambda x: x.tz_localize("America/Chicago"))
points["DATELBL"] = points["DATELBL"].dt.tz_convert('US/Eastern')
points["type"] = "point"
points["icon"] = "circle"
points["markerColor"] = "#333333"
points["title"] = points['DATELBL'].dt.strftime("%b %e") + "<br>" + points['DATELBL'].dt.strftime("%I:%M %p")
points["title"] = points["title"].str.replace("<br>0", "<br>")
points["scale"] = 1.1

points.loc[points["DVLBL"] == "D", "storm_type"] = "Depression"
points.loc[points["DVLBL"] == "H", "storm_type"] = "Hurricane"
points.loc[points["DVLBL"] == "S", "storm_type"] = "Storm"

points["tooltip"] = "On " + points['DATELBL'].dt.strftime("%b %e") + " at " + points['DATELBL'].dt.strftime("%I:%M %p").str.replace("$0", "", regex=True) + " EST, the storm is projected to be classified as a " + points["storm_type"].str.lower() + "."
points["tooltip"] = points["tooltip"].str.replace(" 0", " ")
points["fill"] = "#C42127"
points["markerSymbol"] = points["DVLBL"]

centre_line["type"] = "area"
centre_line["icon"] = "area"
centre_line["fill"] = "#C42127"
centre_line["stroke"] = "#000000"
centre_line["markerColor"] = "#C42127"
centre_line["fill-opacity"] = 0.0
    
probable_path["icon"] = "area"
probable_path["type"] = "area"
probable_path["fill"] = "#6a3d99"
probable_path["stroke"] = "#6a3d99"
probable_path["markerColor"] = "#6a3d99"
probable_path["fill-opacity"] = 0.2

path = pd.concat([centre_line, probable_path, points, data])

path = path[["markerColor", "fill", "fill-opacity", "stroke", "type", "icon", "latitude", "longitude", "geometry", "title", "tooltip", "scale", "markerSymbol"]]
path["latitude"] = path["latitude"].fillna("")
path["longitude"] = path["longitude"].fillna("")

print(path)

hurricane_map = (dwmaps.Map(CHART_ID)
                 .data(path)
                 .head(f"Tracking {name}")
                 .deck(f"Windspeed is currently measured at <b>{windspeed} km/h</b>. The shaded region shows a range of probable paths for the storm over the next five days.")
                 .footer(source="U.S. National Hurricane Center")
                 .publish()
                 )