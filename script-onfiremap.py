import requests
import geopandas
import pandas as pd
import json
import dwmaps

CHART_ID = "L45df"

data = pd.read_csv("https://www.lioapplications.lrc.gov.on.ca/Geocortex/Essentials/essentials411/REST/TempFiles/Export.csv?guid=9cb6d697-f974-45c6-ad57-2aa810642143&contentType=text%2Fcsv")

print(data.columns)

# data["opacity"] = 0.5
# data = data.drop(columns="ID")
# data['id'] = range(0, len(data))
# data["id"] = data['id'].apply(lambda x: f"m{x}")
# data["title"] = ""
# data["type"] = "points"
# data["fill"] = "black"
# data["stroke"] = "black"

# data["icon"] = "fire"

# data["markerColor"] = data["FIRE_STATUS"].replace({"Under Control": "#436170", "New": "#F8C325"})

# data["type"] = "point"

# avg = data["AREA_ESTIMATE"].min()
# std = data["AREA_ESTIMATE"].std()

# data["scale"] = ((data["AREA_ESTIMATE"] - avg) / (std)) + 1
# data["scale"] = data["scale"].apply(lambda x: 2.2 if x > 2.2 else x)

# data["tooltip"] = "<big>" + data['LABEL'] + "</big><br><b>Status</b>: " + data['FIRE_STATUS'] + "</span>"


# print(data.columns)
# chart = dwmaps.DatawrapperMaps(chart_id=CHART_ID)
# dw = (chart
#       .upload(data)
#       .head(f"There are <b>{len(data)} wildfires</b> burning across Alberta")
#       .deck(f"As of today, {round(len(data[data['FIRE_STATUS'] == 'Under Control'])/len(data)*100, 1)}% are listed as under control.", "Government of Alberta")
#       .timestamp()
#       .publish()
#       )