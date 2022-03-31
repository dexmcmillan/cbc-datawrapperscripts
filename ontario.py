import pandas as pd
import requests

## Prepare data.
raw = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv')

ontario = (raw
                 .loc[raw["prname"] == "Ontario", ["date", "numtoday", "numdeathstoday"]]
                 .set_index("date")
                 )

ontario["numtoday_rolling"] = (ontario["numtoday"]
                 .rolling(7).mean()
                 .dropna()
                 )

payload = ontario.to_csv(sep="\t")

## Update chart.
url = "https://api.datawrapper.de/v3/charts/DNm2f/data"

headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": "Bearer f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF",
}

requests.request("PUT", url, headers=headers, data=payload)

## Publish chart.
publish_headers = {
    "Accept": "*/*", 
    "Authorization": "Bearer f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF"
    }

response = requests.request("POST", "https://api.datawrapper.de/v3/charts/DNm2f/publish", headers=publish_headers)

print(response.text)
