

import pandas as pd
import datawrappergraphics

CHART_ID = "j6kHN"


data = pd.read_csv(r"https://www.gov.mb.ca/mit/floodinfo/floodoutlook/forecast_centre/agol/agoldata.csv")

data = data.rename(columns={"Latitude": "latitude", "Longitude": "longitude"})

data = data[data["Alert"] == "Flood Warning"]
data["type"] = "point"
data["icon"] = "circle-sm"

data["type"] = "point"

data['Measured Level (ft)'] = data["Measured Level (ft)"].str.replace(",", "").astype(float)
data['Bankfull Capacity - level (ft)'] = data["Bankfull Capacity - level (ft)"].str.replace(",", "").astype(float)
data["over_capacity"] = data['Measured Level (ft)'] - data['Bankfull Capacity - level (ft)']
data["over_capacity"] = data["over_capacity"].apply(lambda x: round(x, 2))
data.loc[data["over_capacity"] > 0, "over_capacity_dir"] = "over"
data.loc[data["over_capacity"] < 0, "over_capacity_dir"] = "under"

data["markerColor"] = "#29414f"
data.loc[data["over_capacity_dir"] == "over", "markerColor"] = "#29414F"
data.loc[data["over_capacity_dir"] == "under", "markerColor"] = "#C42127"

max = data["over_capacity"].max()
max_name = data.loc[data["over_capacity"] == max, "Station Name"].values[0]

avg = data["over_capacity"].min()
std = data["over_capacity"].std()

data["scale"] = ((data["over_capacity"] - avg) / (std)) + 0.5
data["scale"] = data["scale"].apply(lambda x: 1.8 if x > 1.8 else x)

data["tooltip"] = "Flood warning at <b>" + data['Station Name'].str.strip() + "</b>.<br><br>Water level measured at <b>" + data['Measured Level (ft)'].astype(int).astype(str) + " ft</b>, <b>" + abs(data["over_capacity"]).astype(str) + " ft</b> " + data['over_capacity_dir'] + " the bankfull capacity."

deck = f"<b>{max_name}</b>, the station most over its bankfull capacity, is measured at <b>{max}</b> ft over capacity.<br><br><details><summary><b>What is bankfull capacity?</b></summary>Bankfull capacity is the level at which the water will rise above the banks of the waterway and potentially flood the surrounding area.</details>"

chart = (datawrappergraphics.Map(chart_id=CHART_ID)
            .data(data, append="./assets/shapes/shapes-manitobafloodmap.json")
            .head(f"There are <b>{len(data)} active flood warnings</b> across Manitoba")
            .deck(deck)
            .footer(source="Government of Manitoba")
            .publish()
            )