import requests
from bs4 import BeautifulSoup

url = "https://24timezones.com/es_husohorario/madrid_hora_actual.php"
r = requests.get(url)
print(r) # Response 200

soup = BeautifulSoup(r.content, "html.parser")
# Primero hay que hacer boton derecho, inspeccionar elemento en Google Chrome
cajaFecha = soup.find("span", id="currentTime")
print(cajaFecha.get_text())


