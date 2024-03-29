import pandas as pd
import os
import datawrappergraphics
import geopandas
import glob
import re

# Live chart id: PsIWk
# Test chart id: ioEie
EASTERN_UKRAINE_CHART_ID = "PsIWk"

# Bring in and process shapefile data for Russian advances.

path = os.path.join("./assets/ukraineadvance", "*.zip")

all_files = glob.glob(os.path.join("./assets/ukraineadvance", "*.zip"))

li = []

# Loop through each file and append to list for concat.
for filename in all_files:
    df = geopandas.read_file(filename)
    df["layer"] = re.search("\\\\[a-zA-Z0-9]+\.", filename)[0]
    df["layer"] = df["layer"].str.replace(".", "", regex=True).str.replace("\\", "", regex=True)
    li.append(df)

# Concatenate all shape dataframes together.
areas = pd.concat(li, axis=0, ignore_index=True)

# Filter out any files we don't want included.
areas = areas.loc[~areas["layer"].isin(["ClaimedRussianTerritoryinUkraine", "ClaimedUkrainianCounteroffensives"]),:]

# Define colour for each of the layers (not all of these are included in the import).
areas.loc[areas["layer"].str.contains("ClaimedRussianTerritoryinUkraine"), "markerColor"] = "grey"
areas.loc[areas["layer"].str.contains("ClaimedUkrainianCounteroffensives"), "markerColor"] = "#1f78b4"
areas.loc[areas["layer"].str.contains("UkraineControl"), "markerColor"] = "#c42127"
areas.loc[areas["layer"].str.contains("AssessedRussianAdvances"), "markerColor"] = "#f8c325"

# Define type for area markers.
areas["type"] = "area"

# Define opacity for area markers.
areas["fill-opacity"] = 0.2

# Define fill and stroke colours.
areas["fill"] = areas["markerColor"]
areas["stroke"] = areas["markerColor"]

# Define title.
areas["title"] = areas["layer"]

# Define icon type, which may actually not be necessary!
areas["icon"] = "area"

# Simplify the geometry so it's under 2MB for import into Datawrapper.
areas["geometry"] = areas["geometry"].simplify(1)

# Dissolve so there are only as many shapes as there are files.
areas = areas.dissolve(by="layer")

# Filter out columns we don't need for the visualization.
areas = areas[["title", "geometry", "fill", "stroke", "type", "icon", "fill-opacity"]]

## Import sheet data of points.
raw = (pd
       .read_csv("https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/export?format=csv&gid=0", encoding="utf-8")
       .dropna(how="all", axis=1)
       )

## Rename columns from the spreadsheet.
raw.columns = ["title", "tooltip", "source", "hide_title", "visible", "coordinates", "anchor", "icon"]

print(raw)

## Clean data.
points = (raw
        .dropna(how="all")
        .set_index("title")
        .reset_index()
        )

# Set anchor based on what's specified in spreadsheet.
points["anchor"] = points["anchor"].str.lower()

# Build the tooltip for display.
points["tooltip"] = points["tooltip"].str.strip()
points.loc[points["tooltip"] != "", "tooltip"] = '<b>' + points["title"] + '</b><br>' + points["tooltip"] + ' <i>(Source: ' + points["source"].fillna("").str.strip().str.replace("\"", "'") + ')</i>'

# Define default marker colour for these points.
points["markerColor"] = "#29414F"

# Define default marker type.
points["type"] = "point"

# Define default icon type.
points["icon"] = 'city'

# Define default scale for points.
points["scale"] = 1.2

# Define lat/long for point values.
points["longitude"] = points["coordinates"].apply(lambda x: x.split(", ")[0].replace("[", ""))
points["latitude"] = points["coordinates"].apply(lambda x: x.split(", ")[1].replace("]", ""))

# Specify different marker type for capital city.
points.loc[points["title"] == "Kyiv", "icon"] = "star-2"

# Tweak some label locations for this map only.
points.loc[points["title"] == "Lyman", "anchor"] = "top-center"

# Prepare source string from source column.
points["source"] = points["source"].fillna("")

source_list = set(points["source"].to_list())
source_list_clean = []
for entry in source_list:
    try:
        word = entry.split(", ")
        source_list_clean.append(word)
    except:
        pass

source_list_clean = [item for sublist in source_list_clean for item in sublist]
source_list_clean = [x for x in source_list_clean if x]
source_list_clean = set(source_list_clean)

source_string = ", ".join(source_list_clean) + ", " + "Institute for the Study of War and AEI's Critical Threats Project"

# We only want these cities to show up on the Eastern Ukraine map.
eastern_cities = ["Kyiv", "Kharkiv", "Mariupol", "Mykolaiv", "Kherson", "Odesa", "Kramatorsk", "Bakhmut"]
print(points)
# Bring together points and shapes for import into Datawrapper map.
data = pd.concat([areas, points[points["title"].isin(eastern_cities)]])
data["visible"] = True

print(data)

eastern_ukraine = (datawrappergraphics.Map(chart_id=EASTERN_UKRAINE_CHART_ID)
                    .data(data, "./assets/shapes/shapes-easternukrainemap.json")
                    .head(f"Russia's offensive in Eastern Ukraine")
                    .deck("Tap or hover over a point to read more about fighting in that area.")
                    .footer(note=f"Source: {source_string}.", byline="Wendy Martinez, Dexter McMillan")
                    .publish()
                )