import requests
import json
import os
import datetime
from datawrapper import Datawrapper
import sys

class DatawrapperMaps:
    
    CHART_ID = None
    
    def __init__(self, chart_id):
        self.CHART_ID = chart_id
        
        
        
        
        
        
        
        
        
    def __auth(self):
        try:
            with open('./auth.txt', 'r') as f:
                DW_AUTH_TOKEN = f.read().strip()
        except:
            DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
            
        return DW_AUTH_TOKEN
     
     
     
     
     
     
     
     
     
     
        
    def upload(self, data):
        
        script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
        
        data = data.to_crs("EPSG:4326")
        data.to_file(f"{script_name}.geojson", driver='GeoJSON')
        
        headers = {
            "Authorization": f"Bearer {self.__auth()}"
        }

        with open(f"{script_name}.geojson", 'r') as f:
            geojson = json.load(f)
            
        features = geojson["features"]
        
        new_features = []
        
        for feature in features:
            
            
            new_feature = {}
            
            id = feature["properties"]["id"]
            marker_type = feature["properties"]["type"]
            title = feature["properties"]["title"]
            
            with open(f"assets/{marker_type}.json", 'r') as f:
                new_feature = json.load(f)
                
                new_feature["id"] = id
                new_feature["type"] = marker_type
                new_feature["title"] = title
                new_feature["data"] = feature["properties"]
                
                try: new_feature["tooltip"]["text"] = feature["properties"]["tooltip"]
                except: print(f"Tooltip not specified. Skipping this element.")
                
                for element in ["id", "markerColor", "scale"]:
                        try: new_feature[element] = feature["properties"][element]
                        except: print(f"{element} not specified. Skipping this element.")
                
                if marker_type == "point":
                    new_feature["coordinates"] = feature["geometry"]["coordinates"]     
                else:
                    new_feature["feature"] = feature    

            
                new_features.append(new_feature)
        
        if os.path.exists(f"shapes/shapes-{script_name}.json"):
            with open(f"shapes/shapes-{script_name}.json", 'r') as f:
                bc = json.load(f)
                new_features.append(bc)
            
        payload = {"markers": new_features}

        response = requests.put(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}/data", headers=headers, data=json.dumps(payload))

        print(response)
        
        return self
    
    
    
    
    
    
    
    
    
    
    def head(self, string):


        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        data = {
            "title": string
            }

        response = requests.patch(f"https://api.datawrapper.de/v3/charts/{self.CHART_ID}", headers=headers, data=json.dumps(data))


        print(response.text)
        
        return self
    
    
    
    
    
    
    
    def deck(self, deck, source, byline="Dexter McMillan"):
    

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__auth()}"
        }
        
        dw = Datawrapper(access_token=self.__auth())
        dw.update_description(chart_id=self.CHART_ID, intro=deck, source_name=source, byline=byline)
        
        return self
    
    
    
    
    
    
    
    
    
    
    
    
    
    def timestamp(self):
        
        dw = Datawrapper(access_token=self.__auth())
        
        today = datetime.datetime.today()
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