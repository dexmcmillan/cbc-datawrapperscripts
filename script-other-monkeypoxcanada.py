import pandas as pd
import datawrappergraphics

raw = pd.read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv")

canada = raw[raw["Country"] == "Canada"]
canada[["Location", "City2"]] = canada["Location"].str.split(", ", expand=True)
canada.loc[canada["City"].isna(), "City"] = canada["City2"]

canada = canada.drop("City2", axis=1)

cities = canada.loc[canada["Status"] == "confirmed", ["ID", "City"]].groupby("City").count().sort_values("ID", ascending=False)
cities = cities.head(6)

(datawrappergraphics.Chart("vUriB")
 .data(cities)
 .head(f"Monkeypox cases in Canada")
 .deck(f"Locations with the most confirmed cases.")
 .footer(source="Global.health", timestamp=True)
 .publish()
 )

countries = pd.read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/timeseries-country-confirmed.csv")

canada_time = countries[countries["Country"] == "Canada"]
canada_time = canada_time.drop(["Country", "Cumulative_cases"], axis=1)
canada_time["7-day average"] = canada_time["Cases"].rolling(7).mean()

canada_time = canada_time.dropna()

(datawrappergraphics.Chart("R18TO")
 .data(canada_time)
 .head(f"Monkeypox cases in Canada")
 .deck(f"Rolling 7-day average of confirmed cases since May 2022.")
 .footer(source="Global.health", timestamp=True)
 .publish())