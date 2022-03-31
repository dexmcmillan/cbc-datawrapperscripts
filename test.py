import pandas as pd

sheet_url = "https://docs.google.com/spreadsheets/d/17RIbkQI6o_Y_NZalfqZvB8n_j_AmTV5GoNMuzdbkw3w/edit#gid=0"

url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

raw = pd.read_csv(url_1)

print(raw)