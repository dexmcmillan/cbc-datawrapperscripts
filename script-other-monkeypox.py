import pandas as pd
import datawrappergraphics

WORLD_CHART_ID = "bGaOM"

raw = pd.read_csv("https://raw.githubusercontent.com/owid/monkeypox/main/owid-monkeypox-data.csv")

all_countries = raw.pivot(index="location", columns="date", values="total_cases").dropna(axis=0, how="all")

latest_date = all_countries.columns[-2]

all_countries = all_countries.drop("World").sort_values(latest_date, ascending=False)

all_countries["current_rank"] = range(1, len(all_countries)+1)

world_chart = datawrappergraphics.Chart(chart_id=WORLD_CHART_ID)

meta_obj = {k: "#cccccc" for k in all_countries.index.to_list()}
meta_obj["Canada"] = "#C42127"
meta_obj["United States"] = "#1F78B4"

world_chart.metadata["metadata"]["visualize"]["custom-colors"] = meta_obj
        
(world_chart
    .data(all_countries)
    .head(f"Monkeypox around the world")
    .deck(f"")
    .footer(timestamp=True, byline="Dexter McMillan", source="Our World in Data")
    .publish()
    )