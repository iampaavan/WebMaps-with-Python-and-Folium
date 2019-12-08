import folium, pandas

data = pandas.read_csv("Volcanoes.txt")
latitude = data['LAT']
longitude = data['LON']
elevation = data['ELEV']
name = data['NAME']


def color_producer(elevation):
	if elevation < 1000:
		return 'green'
	elif 1000 <= elevation < 3000:
		return 'orange'
	else:
		return 'red'


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s meters
"""

fgv = folium.FeatureGroup(name='Volcanoes')

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

for lat, long, elev, name in zip(latitude, longitude, elevation, name):
	iframe = folium.IFrame(html=html % (name, name, elev), width=200, height=100)
	map.add_child(folium.Marker(location=[lat, long], popup=folium.Popup(iframe), icon=folium.Icon(color=color_producer(elev))))

fgp = folium.FeatureGroup(name='Population')

map.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
	style_function=lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 10000000
		else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

map.save("Map1.html")
