import pandas as pd
import requests
from zipfile import ZipFile
import requests
from io import BytesIO
from dwmaps import Datawrapper
import os
import json


r = requests.get("https://www150.statcan.gc.ca/n1/en/tbl/csv/18100004-eng.zip?st=G8sPC-61")
files = ZipFile(BytesIO(r.content))
file = files.open(files.namelist()[0])
raw = pd.read_csv(file, encoding="utf-8")

provinces = pd.read_csv("provinces.csv")

gas = raw.loc[(raw["Products and product groups"] == "Gasoline") & (raw["GEO"].isin(provinces["Province"].to_list())) & (raw["REF_DATE"].gt("1980-01-01"))].pivot(values="VALUE", index="REF_DATE", columns="GEO")

print(gas)

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
    
dw = Datawrapper(access_token=DW_AUTH_TOKEN)

headers = {"Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DW_AUTH_TOKEN}"
            }

print(provinces)

# for idx, prov in provinces.iterrows():
    
#     print(prov)
    
#     metadata = {
#         "metadata": {
#             "visualize": {
#                 "legend": {
#                     "enabled": False
#                 }
#             }
#         }
#     }
    
#     df = gas[prov['Province']].rolling(7).mean().reset_index()
#     chart = dw.add_data(data=df, chart_id=prov["chart_id"])
#     requests.patch(f"https://api.datawrapper.de/v3/charts/{prov['chart_id']}", headers=headers, json=metadata)
#     dw.publish_chart(chart_id=prov["chart_id"])
    

# for idx, prov in provinces.iterrows():
#     print(idx, prov)

print(provinces["Province"].to_list())

map_data = (raw
            .loc[(raw["GEO"].isin(provinces["Province"].to_list())) & (raw["REF_DATE"] == raw["REF_DATE"].max()) & (raw["Products and product groups"].isin(["All-items", "Gasoline", "Food"])), ["Products and product groups", "GEO", "VALUE"]]
            .pivot(index="GEO", columns="Products and product groups", values="VALUE")
            )

map_data = map_data.join(provinces.set_index("Province")[["Color", "chart_id", "abbr"]]).reset_index()
map_data["GEO"] = map_data["GEO"].str.replace("Quebec", "Québec")

map_data["text"] = map_data["abbr"] + "<br>" + map_data["All-items"].astype(str)

dw.add_data(data=map_data, chart_id="1YWmn")
dw.publish_chart(chart_id="1YWmn")

print(map_data)

# metadata = {
#     "metadata": {
#         "visualize": {
#         "tooltip": {
#             "title": "<span style='font-weight:bold; color:{{ color }}'>{{ geo }}</span>",
#             "body": "The most recent CPI for <span style='font-weight:bold; color:{{ color }}'>{{ geo }}</span> is <b>{{ all_items }}</b>. The price of gas is measured at <b>{{ gasoline }}</b><hr><img src='http://img.datawrapper.de/{{ chart_id }}/tiny.png' width='200px'>"
#         }
#     }
#     }
# }




# response = requests.patch(f"https://api.datawrapper.de/v3/charts/1YWmn", headers=headers, json=metadata)

# print(response.text)