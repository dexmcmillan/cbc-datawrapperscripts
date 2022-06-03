import datawrappergraphics

CHART_ID = "nSHo0"


hurricane_map = (datawrappergraphics.StormMap(chart_id=CHART_ID, storm_id="AL012022", xml_url="https://www.nhc.noaa.gov/nhc_ep1.xml")
                 .process_data()
                 )

hurricane_map = hurricane_map.data(hurricane_map.dataset)

print(hurricane_map.dataset)

hurricane_map = (hurricane_map
                 .head(f"Tracking {hurricane_map.storm_type.lower()} {hurricane_map.storm_name}")
                 .deck(f"Windspeed is currently measured at <b>{hurricane_map.windspeed} km/h</b>.")
                 .footer(source="U.S. National Hurricane Center")
                 .publish())