import pandas as pd
import datawrappergraphics
import datetime as dt

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

# Live chart ID: Os1m6
MAP_ID = "NyqLI"

# Make HTTP request for the data and put into a geopandas dataframe.
raw = pd.read_csv("https://cwfis.cfs.nrcan.gc.ca/downloads/activefires/activefires.csv")

data = raw.loc[~raw["agency"].isin(["ak", "conus", "pc"]), :]
data.columns = data.columns.str.strip()

data["stage_of_control"] = data["stage_of_control"].str.strip().replace({
    "OC": "Out of control",
    "UC": "Under control",
    "EX": "Extinguished",
    "BH": "Being held"
})

data["province/territory"] = data["agency"].replace({
    "sk": "Saskatchewan",
    "ab": "Alberta",
    "bc": "British Columbia",
    "on": "Ontario",
    "ns": "Nova Scotia",
    "yt": "Yukon",
    "nt": "Northwest Territories",
    "qc": "Quebec",
    "mb": "Manitoba",
    "nl": "Newfoundland and Labrador",
    "pe": "Prince Edward Island"
})

data = data.rename(columns={
    "lat": "Lat",
    "lon": "Lon"
})
data["startdate"] = pd.to_datetime(data["startdate"])

data["duration"] = dt.datetime.today() - data["startdate"]

data = data.sort_values("duration", ascending=False).reset_index()

data["duration"] = data["duration"].apply(lambda x: strfdelta(x, "{days} days and {hours} hours"))


longest_duration = data.at[0, "duration"]

num_fires = len(data)
percent_oc = int(len(data[data["stage_of_control"] == "Out of control"]) / len(data)*100)
total_area = int(data["hectares"].sum())

print(data)

(datawrappergraphics.Chart(MAP_ID)
 .data(data)
 .head(f"There are at least <b>{num_fires:,} active wildfires</b> burning in Canada right now, covering {total_area:,} hectares of land.")
 .deck(f"The longest has been burning for <b>{longest_duration}</b>, and <b>{percent_oc}%</b> are classifed as out of control.<br><br>Size of the circles indicate relative size of the fire. Zoom in to see fires that are closely grouped.")
 .publish()
 )