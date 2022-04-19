import pandas as pd
import os
from datawrapper import Datawrapper

# This code runs differently depending on whether the script is running on a local machine or via Github actions.

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
    
# Read in data from the poll tracker API into a pandas dataframe.

raw = pd.read_csv('https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?pid=1810000401&latestN=0&startDate=19140101&endDate=20221201&csvLocale=en&selectedMembers=%5B%5B2%5D%2C%5B2%2C3%2C79%2C96%2C139%2C176%2C184%2C201%2C219%2C256%2C274%2C282%2C285%2C287%2C288%5D%5D&checkedLevels=')

# Reshape the data a little bit to prepare it for the datawrapper.

filtered = raw[(raw["Products and product groups"] == "All-items")
               & (raw["GEO"] == "Canada")
               & (raw["REF_DATE"] >= "2000-01")
               ]

filtered = (filtered
            .pivot(index="REF_DATE", values="VALUE", columns="Products and product groups")
            .reset_index()
            )

filtered["change"] = (filtered["All-items"].pct_change(12) * 100)

filtered = filtered.dropna(subset=["change"])

filtered["REF_DATE"] = pd.to_datetime(filtered["REF_DATE"])

filtered = filtered.loc[:, ["REF_DATE", "change"]].tail(24)

print(filtered)

# Use the Datawrapper python module to update the data in the chart and publish the changes.
dw = Datawrapper(access_token=DW_AUTH_TOKEN)

dw.add_data(chart_id="9p0ld", data=filtered)
dw.publish_chart(chart_id="9p0ld")