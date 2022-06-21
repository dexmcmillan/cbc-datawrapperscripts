import datawrappergraphics

CHART_ID = "pK1wm"


hurricane_map = (datawrappergraphics.StormMap(chart_id=CHART_ID, storm_id="EP012022", xml_url="https://www.nhc.noaa.gov/nhc_ep1.xml")
                    .data()
                    )
    
hurricane_map = (hurricane_map
                .head(f"TEST: Tracking {hurricane_map.storm_type.lower()} {hurricane_map.storm_name}")
                .deck(f"Windspeed is currently measured at <b>{hurricane_map.windspeed} km/h</b>.<br><br>The dotted line shows the historical path of the weather system.")
                .footer(source="U.S. National Hurricane Center")
                .publish())