import geopandas
import pandas as pd
import datawrappergraphics

CHART_ID = "VJQT3"

raw = geopandas.read_file("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/CY_WildlandFire_Perimeters_ToDate/FeatureServer/0/query?where=irwin_POOCounty%3D%27Los+Angeles%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=")

data = (raw
        .loc[(raw["poly_IncidentName"] == "ROUTE"), ["poly_IncidentName", "irwin_POOState", "irwin_POOCounty", "geometry", "poly_Acres_AutoCalc"]]
        .to_crs("EPSG:4326")
        )

data["fill"] = "#C42127"
data["stroke"] = "#c42127"

highways = geopandas.read_file("https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Freeway_System/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson")
highways["fill"] = False
highways["stroke-width"] = 2.0

highways = highways.loc[highways["ROUTE_NUM"] == "I5"]

data = pd.concat([data, highways])

datawrappergraphics.Map(CHART_ID).data(data, append="./assets/shapes/markers-script-climate-caliwildfires.json").footer(timestamp=True).publish()