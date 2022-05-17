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
            
            icon = ""
            new_feature = {}
            
            if feature["type"] == "area":
        
                new_feature = {'id': feature["properties"]["id"],
                                'data': feature["properties"],
                                'type': feature["properties"]["type"],
                                'title': feature["properties"]["title"],
                                'visible': True,
                                'fill': True,
                                'stroke': True,
                                'exactShape': False,
                                'highlight': False,
                                'icon': icon,
                                'feature': feature,
                                'properties': {'fill': feature["properties"]["fill"],
                                            'fill-opacity': feature["properties"]["opacity"],
                                            'stroke': feature["properties"]["stroke"],
                                            'stroke-width': 1,
                                            'stroke-opacity': 1,
                                            'stroke-dasharray': '100000',
                                            'pattern': 'solid',
                                            'pattern-line-width': 2,
                                            'pattern-line-gap': 2},
                                'visibility': {'mobile': True, 'desktop': True}
                                }
            else:
                with open(f"assets/point.json", 'r') as f:
                    new_feature = json.load(f)
                    new_feature["data"] = feature["properties"]
                    new_feature["id"] = feature["properties"]['id']
                    new_feature["coordinates"] = feature["geometry"]["coordinates"]
                    new_feature["markerColor"] = feature["properties"]["markerColor"]
                    new_feature["scale"] = feature["properties"]["scale"]
                    new_feature["tooltip"]["text"] = feature["properties"]["tooltip"]
            
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