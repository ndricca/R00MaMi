######## still not working ########

import pandas as pd
import folium

with open('bakeka_new.msg', 'rb') as f:
    new_df = pd.read_msgpack(f.read())


mapit = folium.Map(location=[45.464126, 9.189491], zoom_start=13)

for coord in new_df['geo_coord']:
    geo_coord = new_df['geo_coord'].str.split(',', expand=True)
    lat = geo_coord[0]
    lon = geo_coord[1]
    print lat,lon
    folium.Marker(location=[lat, lon]).add_to(mapit)

mapit.save( 'map.html')