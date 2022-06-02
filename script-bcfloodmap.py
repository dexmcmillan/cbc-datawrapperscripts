import requests
import geopandas
import json
from datawrappergraphics.Map import Map
from fiona import errors

# Live chart ID: HufI4
CHART_ID = "HufI4"

# Make request for data from ArcGIS service.
try:
    r = requests.get("https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/services/BC_Flood_Advisory_and_Warning_Notifications_(Public_View)/FeatureServer/0/query?f=json&where=(Basin_Type%20=%20%27Y%27)%20AND%20(Advisory%20%3C%3E%201)&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22:-15196789.939130228,%22ymin%22:6215635.921167677,%22xmax%22:-12403475.17747749,%22ymax%22:8319182.939575167,%22spatialReference%22:{%22wkid%22:102100}}&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID,Major_Basin,Advisory,Sub_Basin,Basin_Type,Comments,Date_Modified&orderByFields=OBJECTID%20ASC&outSR=102100")
    
    # Put into a geopandas dataframe.
    data = geopandas.read_file(json.dumps(r.json()))
    
except errors.DriverError:
    data = geopandas.GeoDataFrame()
    

# Define stroke colour first, based on the advisory type...
data["stroke"] = data["Advisory"].replace(
    {
        1.0: "#e06618",
        2.0: "#e06618",
        3.0: "#e06618"
    })

# ...then define fill based on the stroke colour.
data["fill"] = data["stroke"]

# Title set to the name of the basin.
data["title"] = data["Major_Basin"]

# Define icon and type as areas.
data["type"] = "area"
data["icon"] = "area"


chart = (dwmaps.Map(chart_id=CHART_ID)
        .data(data)
        .head(f"There {'are' if len(data) > 1 else 'is'} <b>{len(data)} flood warning{'s' if len(data) > 1 else ''}</b> across B.C.")
        .footer()
        .publish()
        )