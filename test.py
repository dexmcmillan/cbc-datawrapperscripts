import dwmaps
import pandas as pd
import json

# dwmaps.Map("PsIWk").get_markers(save=True)

# data = pd.read_csv('https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action?pid=1810000401&latestN=0&startDate=19140101&endDate=20221201&csvLocale=en&selectedMembers=%5B%5B2%5D%2C%5B2%2C3%2C79%2C96%2C139%2C176%2C184%2C201%2C219%2C256%2C274%2C282%2C285%2C287%2C288%5D%5D&checkedLevels=')
# data = data.iloc[0:10,:]
# print(data)
# chart = dwmaps.Chart("t5VEu").get_metadata(save=True)

# print(chart)

def get_keys(input_dict):
    for key, value in input_dict.items():
        if isinstance(value, dict):
            for subkey in get_keys(value):
                yield [key, subkey]
        else:
            yield key



feature = {"type": "point", "markerColor": "#c42127", "text": "A test Tooltip!"}

obj = {}

with open(f"./assets/point-fire.json", 'r') as f:
    new_feature = json.load(f)

lis = [key for key in get_keys(new_feature)]

for object in lis:
    if isinstance(object, list):
        obj[object[0]] = {}
        try: obj[object[0]][object[1]] = feature[object[1]]
        except KeyError: obj[object[0]][object[1]] = new_feature[object[0]][object[1]]
    else:
        obj[object] = new_feature[object]

print(obj)