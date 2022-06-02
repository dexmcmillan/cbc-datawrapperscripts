import pandas as pd
from datawrappergraphics.Map import Map

## The ID of the Ukraine map Datawrapper. (LIVE CHART ID: wQIM1. TEST CHART ID: sM21M)
UKRAINE_CHART_ID = "sM21M"

## Import sheet data.
raw = (pd
       .read_csv("https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/export?format=csv&gid=0", encoding="utf-8")
       .dropna(how="all", axis=1)
       )

## Rename columns from the spreadsheet.
raw.columns = ["title", "tooltip", "source", "hide_title", "visible", "coordinates", "anchor", "icon"]

## Clean data.
data = (raw
        .dropna(how="all")
        .set_index("title")
        .reset_index()
        .loc[raw["visible"] == True]
        )

data["source"] = data["source"].fillna("")
data["anchor"] = data["anchor"].str.lower()
data["tooltip"] = data["tooltip"].str.strip()
data["tooltip"] = '<b>' + data["title"] + '</b><br>' + data["tooltip"] + ' <i>(Source: ' + data["source"].fillna("").str.strip().str.replace("\"", "'") + ')</i>'
data["markerColor"] = "#c42127"
data["type"] = "point"
data["icon"] = 'circle-sm'
data["scale"] = 1.2
data["longitude"] = data["coordinates"].apply(lambda x: x.split(", ")[0].replace("[", ""))
data["latitude"] = data["coordinates"].apply(lambda x: x.split(", ")[1].replace("]", ""))
data = data.drop(columns=["coordinates"])

print(data)
data.to_clipboard()

source_list = set(data["source"].to_list())
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
source_string = ", ".join(source_list_clean)

ukraine = (Map(chart_id=UKRAINE_CHART_ID)
    .data(data)
    .head(f"Russian military invasion in Ukraine")
    .deck("")
    .footer(note=f"Source: {source_string}.", byline="Wendy Martinez, Dexter McMillan")
    .publish()
)