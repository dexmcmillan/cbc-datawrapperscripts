import pandas as pd
import datetime as dt
from datawrapper import Datawrapper
import os
import re

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']

dw = Datawrapper(access_token=DW_AUTH_TOKEN)

CHART_ID = "7skMM"

today = dt.datetime.today()
today = today.strftime("%Y-%m-%d")
yesterday = (dt.datetime.today() - dt.timedelta(days=1)).strftime("%b %d, %Y").replace(" 0", " ")
tomorrow = (dt.datetime.today() + dt.timedelta(days=1)).strftime("%Y-%m-%d")

dates = pd.date_range(start=(dt.datetime.today() - dt.timedelta(days=13)), end=(dt.datetime.today() + dt.timedelta(days=2)).strftime("%Y-%m-%d"))
dates = dates.map(lambda x: x.strftime("%Y-%m-%d"))

dfs = []

for date in dates:
    data = pd.read_html(f"https://gaswizard.ca/gas-price-predictions/?pricedate={date}")[0]
    data["date"] = date
    if date == dates[-1]:
        data["Prediction?"] = True
    else:
        data["Prediction?"] = False
    dfs.append(data)


raw = pd.concat(dfs)

raw["City"] = raw["City"].str.replace(":", "")

data = raw.melt(value_vars=["Regular", "Premium", "Diesel"], id_vars=["date", "City", "Prediction?"])

def result_func(x):
    result = re.search("[0-9]+$", x)
    if result:
        return result.group(0)
    else:
        return "0"


data["Price"] = data["value"].astype(str).apply(lambda x: re.search("[0-9]{3}\.[0-9]{1}", x).group(0))
data.loc[data["value"].str.contains(" "), "Change"] = data.loc[data["value"].str.contains(" "), "value"].astype(str).apply(lambda x: result_func(x))

data = data.drop(columns=["value"])

data["Change"] = data["Change"].str.strip().str.replace("⮝", "").str.replace("n/c", "0")

data["Change"] = data["Change"].astype(float)

print(data)

data.loc[data["Change"].gt(0), "Direction"] = "Increase"
data.loc[data["Change"].lt(0), "Direction"] = "Decrease"
data.loc[data["Change"] == 0, "Direction"] = "No change"

data["City"] = data["City"].str.strip()

data.columns = ["Date", "City", "Prediction?", "Fuel Type", "Price", "Change", "Direction"]

data.loc[data["Direction"] == "Decrease", "Text"] = "**" + data['City'] + "**"
data.loc[data["Direction"] == "Increase", "Text"] = "**" + data['City'] + "**"
data.loc[data["Direction"] == "No change", "Text"] = "**" + data['City'] + "**"

data["Text"] = data["Text"].str.replace("\.0", "")

data = data[["Text", "Date", "City", "Fuel Type", "Price", "Change", "Direction", "Prediction?"]]

regular = data.loc[(data["Fuel Type"] == "Regular") & (data["Date"] == dates[-2]), :]

series = data.loc[(data["Fuel Type"] == "Regular")].pivot(columns="Date", index=["City"], values="Price")
series.insert(0, "Today", "")
series.insert(1, "Predicted Value", "")
series.insert(2, "Change", "")
series.insert(3, "Forecast", "")
series["Today"] = series[dates[-2]]
series["Predicted Value"] = series[dates[-1]]
series["Forecast"] = series["Predicted Value"].astype(float) - series["Today"].astype(float)

series["Change"] = series[series.columns[-2]].astype(float).astype(int) - series[series.columns[-3]].astype(float).astype(int)
series = series.merge(regular, right_on="City", left_on="City")
series["City"] = series["Text"]
series = series.drop(columns=["Text", "Date", "Fuel Type", "Price", "Change_y", "Prediction?"]).sort_values("Today", ascending=False)
series.columns = ["City", "Current price", "Predicted Value", "Change_x", "Forecast", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, "Direction"]

series.loc[series["Forecast"].gt(0), "City"] = series["City"] + "<br>Tomorrow: +" + series["Forecast"].astype(str) + " cents"
series.loc[series["Forecast"].lt(0), "City"] = series["City"] + "<br>Tomorrow: " + series["Forecast"].astype(str) + " cents"
series["City"] = series["City"].str.replace("-", "▼")
series["City"] = series["City"].str.replace("+", "▲")

series.loc[series["Forecast"].gt(0), "Predicted Direction"] = "Increase"
series.loc[series["Forecast"].lt(0), "Predicted Direction"] = "Decrease"
series.loc[series["Forecast"] == 0, "Predicted Direction"] = "No change"

print(series)

dw.add_data(chart_id=CHART_ID, data=series)
dw.publish_chart(chart_id=CHART_ID)