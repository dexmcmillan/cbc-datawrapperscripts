import pandas as pd
import requests

raw = pd.read_csv('https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?pid=1810000401&latestN=0&startDate=20100101&endDate=&csvLocale=en&selectedMembers=%5B%5B2%5D%2C%5B2%2C3%2C79%2C96%2C139%2C176%2C184%2C201%2C219%2C256%2C274%2C282%2C285%2C287%2C288%5D%5D')
data = raw.loc[raw["Products and product groups"] == "All-items", :].pivot(index="REF_DATE", columns="Products and product groups", values="VALUE")
data.index = pd.to_datetime(data.index)
payload = data.to_csv(sep="\t")

url = "https://api.datawrapper.de/v3/charts/BM87z/data"

headers = {
    "Accept": "*/*",
    "Content-Type": "text/csv",
    "Authorization": "Bearer f8uy8xNbIvpvFnMdTrcMnHuAPCuhF1epwSxEvEpfTrj0ngPEqLTM6DeZMCYaCsjF",
}


requests.request("PUT", url, headers=headers, data=payload)