import pandas as pd
import requests

CHART_ID = "GYSVs"
AUTH_TOKEN = "f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF"

## Prepare data.
raw = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv')

alberta = (raw
                 .loc[raw["prname"] == "Alberta", ["date", "numtoday", "numdeathstoday"]]
                 .set_index("date")
                 )

alberta["numtoday_rolling"] = (alberta["numtoday"]
                 .rolling(7).mean()
                 .dropna()
                 )

payload = alberta.to_csv(sep="\t")

## Update chart.
url = f"https://api.datawrapper.de/v3/charts/{CHART_ID}/data"

headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

requests.request("PUT", url, headers=headers, data=payload)

## Publish chart.
publish_headers = {
    "Accept": "*/*", 
    "Authorization": f'Bearer {AUTH_TOKEN}'
    }

response = requests.request("POST", f"https://api.datawrapper.de/v3/charts/{CHART_ID}/publish", headers=publish_headers)
