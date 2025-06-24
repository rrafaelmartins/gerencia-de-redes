import json
import requests
import folium
from folium.plugins import HeatMap
import time

# Carrega o arquivo com as rotas
with open("rotas.json", "r") as f:
    rotas = json.load(f)

geo_cache = {}

def geolocate_ip(ip):
    if ip in geo_cache:
        return geo_cache[ip]
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res['status'] == 'success':
            coords = (res['lat'], res['lon'])
            geo_cache[ip] = coords
            return coords
    except:
        pass
    geo_cache[ip] = None
    return None

mapa = folium.Map(
    location=[20, 0],  
    zoom_start=2,
    tiles='OpenStreetMap'  
)

folium.TileLayer(
    tiles='CartoDB positron',
    name='CartoDB Positron'
).add_to(mapa)

folium.TileLayer(
    tiles='CartoDB dark_matter',
    name='CartoDB Dark Matter'
).add_to(mapa)

folium.TileLayer(
    tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
    attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors',
    name='Stamen Terrain'
).add_to(mapa)

folium.TileLayer(
    tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
    attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors',
    name='Stamen Toner'
).add_to(mapa)

coordenadas_nos = []
coordenadas_rotas = []

print("Processando traceroutes...")
count = 0

for site, rota in rotas.items():
    print(f"Processando {site}...")
    coords_rota = []
    
    for ip in rota:
        if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172."):
            continue
            
        loc = geolocate_ip(ip)
        if loc:
            count += 1
            lat, lon = loc
            coords_rota.append([lat, lon])
            coordenadas_nos.append([lat, lon])
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=f'IP: {ip}<br>Site: {site}',
                color='blue',
                fill=True,
                fillColor='lightblue',
                fillOpacity=0.7
            ).add_to(mapa)
            
            print(f"{count} - Sucesso: {ip} -> {lat}, {lon}")
        else:
            print(f"Falha na geolocalização: {ip}")
    
    if len(coords_rota) > 1:
        folium.PolyLine(
            locations=coords_rota,
            color='red',
            weight=2,
            opacity=0.6,
            popup=f'Rota para {site}'
        ).add_to(mapa)
    
    coordenadas_rotas.extend(coords_rota)
    time.sleep(0.1)  

if coordenadas_nos:
    heat_map = HeatMap(coordenadas_nos, radius=15, blur=10)
    heat_map.add_to(mapa)

folium.LayerControl().add_to(mapa)

folium.Marker(
    location=[60, -100],
    popup=f'''
    <b>Topologia Global de Traceroutes</b><br>
    Total de IPs mapeados: {len(coordenadas_nos)}<br>
    Sites analisados: {len(rotas)}<br>
    <br>
    <b>Legendas:</b><br>
    AZUL - Nós da rede<br>
    VERMELHO - Rotas de conexão<br>
    ÁREAS PINTADAS - Mapa de calor (densidade)
    ''',
    icon=folium.Icon(color='green', icon='info-sign')
).add_to(mapa)

print(f"\nSalvando mapa interativo...")
mapa.save('mapa_interativo_traceroutes.html')
