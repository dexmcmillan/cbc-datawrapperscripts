import pandas as pd
import requests

CHART_IDS = [
            "DNm2f", # Ontario
            "BPmg4", # Alberta
            "3rONz", # Manitoba
            "PIVxK", # New Brunswick
            "34VzE", # BC
            "9H3Bn", # Canada
             ]

AUTH_TOKEN = "f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF"

## Prepare data.
raw = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv')

all = (raw
            .pivot(columns="prname", index="date", values="numtoday")
            .rolling(7).mean()
            .dropna()
            )

print(all)

payload = all.to_csv(sep="\t")



headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

publish_headers = {
    "Accept": "*/*", 
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

for id in CHART_IDS:
    ## Update chart.
    requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{id}/data", headers=headers, data=payload)
    
    ## Publish chart.
    response = requests.request("POST", f"https://api.datawrapper.de/v3/charts/{id}/publish", headers=headers)
    response






print(response.text)
