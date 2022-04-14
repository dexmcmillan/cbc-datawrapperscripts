import geopandas
import pandas as pd
import fiona

fiona.supported_drivers['KML'] = 'rw'

assessed_advance = geopandas.read_file("warmaps/AssessedRussianAdvanceInUkraineAPR13.zip")
claimed_territory = geopandas.read_file("warmaps/ClaimedRussianTerritoryinUkraineAPR13.zip")
counter = geopandas.read_file("warmaps/ClaimedUkrainianCounterOffensives13APR.zip")
ukraine_control = geopandas.read_file("warmaps/UkraineCOntrolMapAO13APR2022.zip")

assessed_advance[["color", "fill-color"]] = "#C42127"
claimed_territory["color"] = "#F8C325"
counter["color"] = "#1F78B4"
ukraine_control["color"] = "#C42127"

data = (pd
 .concat([assessed_advance, claimed_territory, ukraine_control])
 .loc[:, ["geometry", "color"]]
 .to_crs(crs="EPSG:4326")
 )

data.to_file("warmaps/ukraineadvance-export.geojson", driver='GeoJSON')
data.to_file("warmaps/ukraineadvance-export.kml", driver='KML')