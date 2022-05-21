import requests
import json
import os
import datetime
from datawrapper import Datawrapper
import sys
import pandas as pd
import geopandas


class DatawrapperMaps:
    
    
    CHART_ID = None
    script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
    filename = f"{script_name}.geojson"
    
    def __init__(self, chart_id):
        self.CHART_ID = chart_id
        
        
        
        
        
        
        
    def __auth(self):
        
        
        try:
            with open('./auth.txt', 'r') as f:
                DW_AUTH_TOKEN = f.read().strip()
                
        except: DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
            
        return DW_AUTH_TOKEN
     
     
     
     
     
    def df_to_geojson(self, dframe, lat='latitude', lon='longitude'):
        print(dframe)
        # create a new python dict to contain our geojson data, using geojson format
        geojson = {'type':'FeatureCollection', 'features':[]}

        # loop through each row in the dataframe and convert each row to geojson format
        for _, row in dframe.iterrows():
            # create a feature template to fill in
            feature = {'type':'Feature',
                    'properties':{},
                    'geometry':{'type':'Point',
                                'coordinates':[]}}

            # fill in the coordinates
            feature['geometry']['coordinates'] = [row[lon],row[lat]]

            # for each column, get the value and add it as a new feature property
            for prop in dframe.columns:
                feature['properties'][prop] = row[prop]
            
            # add this feature (aka, converted dataframe row) to the list of features inside our dict
            geojson['features'].append(feature)
        
        return geojson
     
     
     
     
        
    def upload(self, data):
        
        headers = {"Authorization": f"Bearer {self.__auth()}"}
        
        data['id'] = range(0, len(data))
        data["id"] = data['id'].apply(lambda x: f"m{x}")
        
        if isinstance(data, pd.DataFrame) and not isinstance(data, geopandas.GeoDataFrame):
            print(f"Pandas df detected.")
            data = self.df_to_geojson(data)
        else:
            data = data.to_crs("EPSG:4326")
            data = json.loads(data.to_json())
        
        features = data["features"]
        
        new_features = []
        
        for feature in features:
            
            new_feature = {
                    "id": feature["properties"]["id"],
                    "type": feature["properties"]["type"],
                    "data": feature["properties"],
                    "icon": feature["properties"]["icon"]
                }
            
            with open(f"assets/{new_feature['type']}{'-' + new_feature['icon'] if new_feature['type'] == 'point' else ''}.json", 'r') as f:
                
                new_feature = json.load(f)
                
                try: new_feature["tooltip"]["text"] = feature["properties"]["tooltip"]
                except: print(f"Tooltip not specified. Skipping this element.")
                
                for element in ["markerColor", "scale", "title", "id"]:
                    try: new_feature[element] = feature["properties"][element]
                    except: print(f"{element} not specified. Skipping this element.")
                
                if new_feature['type'] == "point":
                    new_feature["coordinates"] = feature["geometry"]["coordinates"]
                    new_feature["markerColor"] = feature["properties"]["markerColor"]
                else:
                    new_feature["feature"] = feature    

                new_features.append(new_feature)
        
        if os.path.exists(f"assets/shapes/shapes-{self.script_name}.json"):
            with open(f"assets/shapes/shapes-{self.script_name}.json", 'r') as f:
                bc = json.load(f)
                new_features.append(bc)
            
        payload = {"markers": new_features}
        payload = json.dumps(payload)

        response = requests.put(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers, data=payload)

        print(response)
        
        return self
    
    
    
    
    
    
    
    
    
    
    def head(self, string):

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        data = {"title": string}
        data = json.dumps(data)
        
        response = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=data)

        print(response.text)
        
        return self
    
    
    
    
    
    
    
    
    
    
    def deck(self, deck, source, byline="Dexter McMillan"):
        
        dw = Datawrapper(access_token=self.__auth())
        dw.update_description(chart_id=self.CHART_ID, intro=deck, source_name=source, byline=byline)
        
        return self
    
    
    
    
    
    
    
    
    
    
    
    
    
    def timestamp(self):
        
        dw = Datawrapper(access_token=self.__auth())
        
        os_name = os.name
        
        today = datetime.datetime.today()
        
        if os_name == "posix":
            today = today - datetime.timedelta(hours=4)
        
        time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."
        day = today.strftime('%B %d, %Y')
        
        
    

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        note = f"Last updated on {day} at {time}".replace(" 0", " ")
        
        data = {
            "annotate": {
                "notes": note,
            }
        }

        requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(data))
        dw.update_metadata(chart_id=self.CHART_ID, properties=data)
        
        return self
    
    
    
    
    
    
    
    
    
    def publish(self):
        
        dw = Datawrapper(access_token=self.__auth())
        
        dw.publish_chart(chart_id=self.CHART_ID)
        
        return self
    
    
    
    
    
    
    def get_markers(self, save=False):
        
        headers = {
            "Accept": "text/csv",
            "Authorization": f"Bearer {self.__auth()}"
            }
        
        print(self.CHART_ID)
        response = requests.get(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers)
        markers = response.json()["markers"]
        
        if save:
            with open(f"markers-{self.script_name}.json", 'w') as f:
                json.dump(markers, f)
                
        return markers