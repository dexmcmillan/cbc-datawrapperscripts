import pandas as pd
import requests
import os

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']

CHART_IDS = [
            "DNm2f", # Ontario
            "BPmg4", # Alberta
            "3rONz", # Manitoba
            "PIVxK", # New Brunswick
            "34VzE", # BC
            "9H3Bn", # Canada
            "pmp9T", # Saskatchewan
             ]

if 'DW_AUTH_TOKEN' in os.environ:
    AUTH_KEY = os.environ['DW_AUTH_TOKEN']
else:
    AUTH_KEY = DW_AUTH_TOKEN

## Prepare data.
raw = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv')

all = raw.pivot(columns="prname", index="date", values="numtoday")
all["atlantic"] = all["Newfoundland and Labrador"] + all["New Brunswick"] + all["Nova Scotia"] + all["Prince Edward Island"]

all = all.rolling(7).mean().dropna()

print(all)

payload = all.to_csv(sep="\t")

headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": f"Bearer {AUTH_KEY}",
}

publish_headers = {
    "Accept": "*/*", 
    "Authorization": f"Bearer {AUTH_KEY}"
}

for id in CHART_IDS:
    ## Update chart.
    requests.request("PUT", f"https://api.datawrapper.de/v3/charts/{id}/data", headers=headers, data=payload)
    
    ## Publish chart.
    response = requests.request("POST", f"https://api.datawrapper.de/v3/charts/{id}/publish", headers=headers)






print(response.text)
