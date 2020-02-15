
import urllib.parse
import urllib.request
import json


serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

def devuelve_coordenadas():
    print('\n')
    address = input('Ciudad a buscar: ')
    url = serviceurl + urllib.parse.urlencode({'sensor':'false','address':address,'key':'AIzaSyDRDhPvMeDqkojPCVvKeTr471lWM-thXr4'})
    #print('Recuperando los datos de la ciudad', url)
    uh = urllib.request.urlopen(url)
    data = uh.read()
    #print('Recuperados',len(data),'caracteres')
    try: js = json.loads(data)
    except: js = None
    if "status" not in js or js['status'] != 'OK':
        print('==== Fallo de recuperación ====')
        #print(data)
    #print(json.dumps(js, indent=4))
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    print('lat:', lat, 'lng', lng)
    location = js['results'][0]['formatted_address']
    print(location + '\n')
    return lat, lng

def catastro(lat_to_search, lon_to_search):
    from selenium import webdriver
    driver = webdriver.Chrome()
    url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx"
    driver.get(url)

    # Hacer click en un enlace
    coord = driver.find_element_by_link_text("COORDENADAS")
    coord.click()

    lat = driver.find_element_by_id("ctl00_Contenido_txtLatitud")
    lon = driver.find_element_by_id("ctl00_Contenido_txtLongitud")

    from selenium.webdriver.common.action_chains import ActionChains
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(lat).click(lat) # Para provocar el click en la caja y que salte el JavaScript
    lat.send_keys(str(lat_to_search))
    ActionChains(driver).move_to_element(lon).click(lon) # Para provocar el click en la caja y que salte el JavaScript
    lon.send_keys(str(lon_to_search))

    # Pulsamos botones
    datos = driver.find_element_by_id("ctl00_Contenido_btnDatos")
    datos.click()


    html = driver.find_element_by_xpath("/html") # / se usa para referirnos al pricipio del documento (camino absoluto)
    print("##################print(html.text)#####################")
    print(html)

    hijos = driver.find_elements_by_xpath("/html/body/*") # No nos importa el nombre del elto en concreto
    print("####################print(element.tag_name)##################")
    for i, element in enumerate(hijos):
        print(f'Elemento {i}: ' + element.text + '\n')




    # Cuando hayamos terminado de usar Selenium convene cerrar el driver para liberar recursos
    driver.close()


lat, lon = devuelve_coordenadas()

catastro(lat,lon)