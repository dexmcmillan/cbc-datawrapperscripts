import pandas as pd
import datawrappergraphics

CHART_ID = "Cx3zg"

raw = pd.read_csv('https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?pid=1810000401&latestN=0&startDate=19140101&endDate=20221201&csvLocale=en&selectedMembers=%5B%5B2%5D%2C%5B2%2C3%2C79%2C96%2C139%2C176%2C184%2C201%2C219%2C256%2C274%2C282%2C285%2C287%2C288%5D%5D&checkedLevels=')

# Reshape the data a little bit to prepare it for the datawrapper.

filtered = raw[(raw["Products and product groups"] == "All-items")
               & (raw["GEO"] == "Canada")
               & (raw["REF_DATE"] >= "2020-01-01")
               ]

filtered = (filtered
            .pivot(index="REF_DATE", values="VALUE", columns="Products and product groups")
            .reset_index()
            )

filtered["change"] = (filtered["All-items"].pct_change(12) * 100)

filtered = filtered.dropna(subset=["change"])

filtered["REF_DATE"] = pd.to_datetime(filtered["REF_DATE"])

filtered = filtered.loc[:, ["REF_DATE", "change"]].set_index("REF_DATE")

print(filtered)

chart = datawrappergraphics.Chart(chart_id=CHART_ID).data(filtered).publish()