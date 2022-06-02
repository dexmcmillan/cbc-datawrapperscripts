from datawrappergraphics.StormMap import StormMap

CHART_ID = "nSHo0"


hurricane_map = (StormMap(chart_id=CHART_ID, storm_id="ep012022")
                 .process_data()
                 )

hurricane_map = hurricane_map.data(hurricane_map.dataset)

print(hurricane_map.dataset)

hurricane_map = (hurricane_map
                 .head(f"Tracking {hurricane_map.storm_type.lower()} {hurricane_map.storm_name}")
                 .deck(f"Windspeed is currently measured at <b>{hurricane_map.windspeed} km/h</b>.")
                 .footer(source="U.S. National Hurricane Center")
                 .publish())