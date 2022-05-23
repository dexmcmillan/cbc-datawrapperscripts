import requests
import json
import os
import datetime
import sys
import pandas as pd
import geopandas
from typing import Union


class DatawrapperGraphic:
# This is the parent class for all datawrapper graphics.
    
    global CHART_ID
    global metadata
    
    def __init__(self, chart_id: str = None, copy_id: str = None):
        
        headers = {
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
            }
        
        # If no chart ID is passed, and no copy id is passed, we create a new chart from scratch.
        if chart_id == None and copy_id == None:
            
            print(f"No chart specified. Creating new chart...")

            response = requests.post(f"https://api.datawrapper.de/v3/charts/", headers=headers)
            
            chart_id = response.json()["publicId"]

            print(f"New chart created with id {chart_id}")
            
            DatawrapperGraphic.CHART_ID = chart_id
        
        # If we want to make a copy of a graphic to create the new graphic.    
        elif chart_id == None and copy_id != None:
            
            print(f"No chart specified. Copying chart with ID: {copy_id}...")
            
            response = requests.post(f"https://api.datawrapper.de/v3/charts/{id}/copy", headers=headers)
            chart_id = response.json()["publicId"]
            
            print(f"New chart ({chart_id}) created as a copy of {copy_id}.")
            
            DatawrapperGraphic.CHART_ID = chart_id
            
        # If we specify a chart id and no copy id, then there is a chart already made that we're altering.    
        elif chart_id != None and copy_id == None:
            
            DatawrapperGraphic.CHART_ID = chart_id
        
        # Throw exception if both copy id and chart id are input.    
        elif chart_id != None and copy_id != None:
            raise Exception(f"Please specify either a chart_id or a copy_id, but not both.")
        
        response = requests.get(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}", headers=headers)
        self.metadata = response.json()

    
    
    
    def settings(self):
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
        }

        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}", headers=headers, data=json.dumps(self.metadata))
        
        
        if r.ok:
            print(f"SUCCESS: Metadata updated.")
        else:
            raise Exception(f"Couldn't update metadata. Response: {r.reason}")
        
        return self
    
    
    
    
    def head(self, string: str):
    
        # Define headers for headline upload.
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
        }
        
        # Take the string input as a parameter and put it into a payload object. Then convert to JSON string.
        data = {"title": string}
        data = json.dumps(data)
        
        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}", headers=headers, data=data)
        
        if r.ok:
            print(f"SUCCESS: Chart head added.")
        else:
            raise Exception(f"Chart head was not added. Response: {r.text}")
        
        return self
    
    
    
    
    
    
    

    
    def deck(self, deck: str):
        
        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
            }
        
        payload =  {
            "metadata": {
                "describe": {
                    "intro": deck,
                },
            }
        }
        
        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}", headers=headers, data=json.dumps(payload))
        
        if r.ok:
            print(f"SUCCESS: Chart deck added.")
        else:
            raise Exception(f"Chart deck was not added. Response: {r.text}")
        
        return self
    
    
    
    
    
    
    
    
    
    ## Adds a timestamp to the "notes" section of your chart. Also allows for an additional note string that will be added before the timestamp.
    
    def footer(self, source: str, byline:str = "Dexter McMillan", note: str = "", timestamp: bool = True):
        
        os_name = os.name
        
        today = datetime.datetime.today()
        
        if os_name == "posix":
            today = today - datetime.timedelta(hours=4)
        
        time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."
        day = today.strftime('%B %d, %Y')
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
        }
        
        timestamp_string = f"Last updated on {day} at {time}.".replace(" 0", " ")
        
        data =  {
            "metadata": {
                "describe": {
                    "source-name": source,
                    "byline": byline,
                },
                "annotate": {
                    "notes": f"{note} {timestamp_string if timestamp else ''}".strip(),
                },
            }
        }

        r = requests.patch(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}", headers=headers, data=json.dumps(data))
        
        
        if r.ok:
            print(f"SUCCESS: Chart footer (byline, notes, and source) built and added.")
        else:
            raise Exception(f"Couldn't build chart footer. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    
    
    
    def publish(self):

        headers = {
            "Accept": "*/*", 
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
            }

        r = requests.post(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}/publish", headers=headers)
        
        if r.ok:
            print(f"SUCCESS: Chart published!")
        else:
            raise Exception(f"Chart couldn't be published. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    
    
    
    
    def auth():
        
        # On a local machine, it will read the auth.txt file for the token.
        try:
            with open('./auth.txt', 'r') as f:
                DW_AUTH_TOKEN = f.read().strip()
        # If this is run using Github actions, it will take a secret from the repo instead.        
        except FileNotFoundError: DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
            
        return DW_AUTH_TOKEN 
    
    
    
    
    

class Chart(DatawrapperGraphic):
    
    # Use this class to create a new, copy, or to manage a currently existing Datawrapper chart (ie. not a map!).
    
    script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
    
    
    
    
    
    def __init__(self, chart_id: str = None, copy_id: str = None):
        super().__init__(chart_id, copy_id)
    
    
    
    
    
    
    def data(self, data: pd.DataFrame):
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "text/csv",
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
        }

        payload = data.to_csv()
        
        r = requests.put(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}/data", headers=headers, data=payload)

        if r.ok:
            print(f"SUCCESS: Data added to chart.")
        else:
            raise Exception(f"Chart data couldn't be added. Response: {r.reason}")
        
        return self
    
    
    
    
    
    




class Map(DatawrapperGraphic):
    
    
    script_name = os.path.basename(sys.argv[0]).replace(".py", "").replace("script-", "")
    
    
    def __init__(self, chart_id: str = None, copy_id: str = None):
        super().__init__(chart_id, copy_id)
        
     
     
     
     
     ## This function converts a pandas dataframe into geojson if the data you're using doesn't import correctly into Geopandas.
     
    def df_to_geojson(self, dframe: pd.DataFrame, lat: str = 'latitude', lon: str = 'longitude'):
        
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
     
     
     
     
     
     
     
     
        
    def data(self, data: Union[pd.DataFrame, geopandas.GeoDataFrame]):
        
        ## The essence of this function, which does the majority of the heavy lifting in this class, is to turn the dataframe to a json object, iterate over the important properties, and place them in a template geojson that will then be uploaded to Datawrapper through the API.
        
        headers = {"Authorization": f"Bearer {DatawrapperGraphic.auth()}"}
        
        # Create an id column that uses Datawrapper's ID naming convention.
        data['id'] = range(0, len(data))
        data["id"] = data['id'].apply(lambda x: f"m{x}")
        
        # Check if the data input is a pandas dataframe or a geopandas dataframe. if it's pandas, call df_to_geojson(). If not, convert crs and convert geopandas to json.
        # The outcome of this if/else is a list of json objects that can be iterated through.
        if not isinstance(data, geopandas.GeoDataFrame):
            print(f"Pandas df detected.")
            data = self.df_to_geojson(data)
        else:
            data = data.to_crs("EPSG:4326")
            data = json.loads(data.to_json())
        
        # Get only the features from the object.
        features = data["features"]
        
        # New list for storing the altered geojson.
        new_features = []
        
        for feature in features:
            
            # Take the important properties from the dataframe's json object.
            try: icon = feature["properties"]['icon']
            except KeyError: raise Exception(f"Icon was not specified in your file. Please add a column for this property.")
            
            try: marker_type = feature["properties"]["type"]
            except KeyError: raise Exception(f"Marker type was not specified in your file. Please add a column for this property.")
            
            # Load the template feature object depending on the type of each marker (area or point).
            with open(f"assets/{marker_type}{'-' + icon if marker_type == 'point' else ''}.json", 'r') as f:
                
                new_feature = json.load(f)
                
                # Take the important properties from the dataframe's json object.
                new_feature["id"] = feature["properties"]["id"]
                
                for element in ["markerColor", "scale", "title", "id", "anchor"]:
                    try: new_feature[element] = feature["properties"][element]
                    except KeyError: pass
                
                if marker_type == "point":
                    
                    try: new_feature["tooltip"]["text"] = feature["properties"]["tooltip"]
                    except KeyError: pass
                    
                    try: new_feature["coordinates"] = feature["geometry"]["coordinates"]
                    except TypeError: new_feature["coordinates"] = [float(feature["properties"]["longitude"]), float(feature["properties"]["latitude"])]
                    
                    new_feature["markerColor"] = feature["properties"]["markerColor"]
                    
                else:
                    new_feature["feature"] = feature
                    
                    for element in ["fill", "stroke", "fill-opacity"]:
                    
                        try: new_feature["properties"][element] = feature["properties"][element]
                        except KeyError: pass

                new_features.append(new_feature)
        
        # If there are other shapes to be added (ie. highlights of provinces, etc.) then this will use a naming convention to grab them from the shapes folder.
        if os.path.exists(f"assets/shapes/shapes-{self.script_name}.json"):
            with open(f"assets/shapes/shapes-{self.script_name}.json", 'r') as f:
                shapes = json.load(f)
                if type(shapes) != list:
                    shapes = [shapes]
                for shape in shapes:
                    new_features.append(shape)
        
        # Change layout of the markers to match what Datawrapper likes to receive.    
        payload = {"markers": new_features}
        payload = json.dumps(payload)

        r = requests.put(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}/data", headers=headers, data=payload)

        if r.ok:
            print(f"SUCCESS: Data added to chart.")
        else:
            raise Exception(f"Chart data couldn't be added. Response: {r.reason}")
        
        return self
    
    
    
    
    
    
    
    
    
    
    def get_markers(self, save: bool = False):
        
        headers = {
            "Accept": "text/csv",
            "Authorization": f"Bearer {DatawrapperGraphic.auth()}"
            }
        
        print(DatawrapperGraphic.CHART_ID)
        response = requests.get(f"https://api.datawrapper.de/v3/charts/{DatawrapperGraphic.CHART_ID}/data", headers=headers)
        markers = response.json()["markers"]
        
        if save:
            with open(f"markers-{self.script_name}.json", 'w') as f:
                json.dump(markers, f)
                
        return markers