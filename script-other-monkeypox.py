import pandas as pd
import datawrappergraphics
import numpy as np
import logging

WORLD_CHART_ID = "bGaOM"
CANADA_CHART_ID = "qeH8o"
FIB_CHART_ID = "Em8sO"

raw_cases = pd.read_csv("https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv", encoding="utf-8")

data = raw_cases[raw_cases["Status"].isin(["confirmed", "suspected"])].sample(frac=1)

for col, values in data.iteritems():
    data[col] = data[col].astype(str).str.replace("ʻ", "")
    
canada_percent = str(round((len(data[data["Country"] == "Canada"]) / len(data) *100), 1))


fib_chart = (datawrappergraphics.FibonacciChart(chart_id=FIB_CHART_ID)
             .data(data)
             .head(f"Confirmed and suspected monkeypox cases around the world")
             .deck(f"<b>{canada_percent}%</b> of worldwide cases have been in Canada.")
             .publish()
             )

raw = pd.read_csv("https://raw.githubusercontent.com/owid/notebooks/main/EdouardMathieu/monkeypox/owid-monkeypox-data.csv")

all_countries = raw.pivot(index="location", columns="date", values="total_confirmed_by_confirmation").dropna(axis=0)

latest_date = all_countries.columns[-1]

all_countries = all_countries.drop("World").sort_values(latest_date, ascending=False)

all_countries["current_rank"] = range(1, len(all_countries)+1)

canada_rank = all_countries[["current_rank"]].at["Canada", "current_rank"]

match canada_rank:
    case 1:
        suffix = "st"
    case 2:
        suffix = "nd"
    case 3:
        suffix = "rd"
    case _:
        suffix = "th"
        
world_chart = (datawrappergraphics.Chart(chart_id=WORLD_CHART_ID)
    .data(all_countries)
    .head(f"Monkeypox around the world")
    .deck(f"<span style='color:#C42127;font-weight:500'>Canada</span> is currently ranked <b>{canada_rank}{suffix}</b> worldwide in terms of daily cases.")
    .publish()
    )

canada = raw.loc[raw["location"] == "Canada", ["date", "total_all_by_entry"]]
logging.info(canada)

canada_chart = (datawrappergraphics.Chart(chart_id=CANADA_CHART_ID)
    .data(canada)
    .head(f"Confirmed and suspected monkeypox cases in <span style='color:#C42127'>Canada</span>")
    .deck(f"Canada is currently ranked <b>{canada_rank}{suffix}</b> in terms of daily cases.")
    .publish()
    )