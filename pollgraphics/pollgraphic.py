import pandas as pd
import requests
import os
from datawrapper import Datawrapper

# This code runs differently depending on whether the script is running on a local machine or via Github actions.

try:
    from config import DW_AUTH_TOKEN
except ModuleNotFoundError:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
    
# Read in data from the poll tracker API into a pandas dataframe.

raw = requests.get("https://canopy.cbc.ca/live/poll-tracker/v4/CAN").json()['data']

# Reshape the data a little bit to prepare it for the datawrapper.

data = (pd
         .json_normalize(raw, record_path=['pollsters', 'rows', 'data'], meta=[['pollsters', 'rows', 'pollster'], ['pollsters', 'rows', 'start_date'], ['pollsters', 'rows', 'end_date']])
         .pivot_table(columns="party", index="pollsters.rows.pollster", values="seats", aggfunc="mean")
         .reset_index()
)

# Use the Datawrapper python module to update the data in the chart.

dw = Datawrapper(access_token=DW_AUTH_TOKEN)

dw.add_data(chart_id="keAsd", data=data)