# @author: Carlos Rabazo
# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import json

serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
while True:
    address = input('Entrar ciudad: ')
    if len(address) < 1 : break
    url = serviceurl + urllib.parse.urlencode({'sensor':'false','address':address,'key':'AIzaSyDRDhPvMeDqkojPCVvKeTr471lWM-thXr4'})
    print('Recuperando los datos de la ciudad', url)
    uh = urllib.request.urlopen(url)
    data = uh.read()
    print('Recuperados',len(data),'caracteres')
    try: js = json.loads(data)
    except: js = None
    if "status" not in js or js['status'] != 'OK':
        print('==== Fallo de recuperación ====')
        print(data)
        continue
    print(json.dumps(js, indent=4))
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    print('lat:', lat, 'lng', lng)
    location = js['results'][0]['formatted_address']
    print(location)