
import urllib.parse
import urllib.request
import json


serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

def devuelve_coordenadas():
    address = input('Entrar ciudad: ')
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
    print(location)
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
    print(html.text)

    # Flexibilidad de XPath es que permite encadenar varios pasos
    head = driver.find_element_by_xpath("/html/head")
    body = driver.find_element_by_xpath("/html/body")
    # Excepcion NoSuchElementException si no lo encuentra (usar try catch)
    # IMPORTANTE: Cualquier busqueda en selenium devuelve un elemento de tipo WebElement que es un puntero al elemento
    # seleccionado. La variable no contiene al elemento, lo señala
    html2 = body.find_element_by_xpath("/html") # Usamos body y no driver como punto de partida para demostrar que podemos
    # forzar a acceder de nuevo a la raiz y tomar el elemento html (se puede hacer por ser un señalador
    # OJO: driver.execute_script("window.history.go(-1)")
    # print(body.text) no funcionaria

    # COMPONENTE *
    # Nombre de los elementos que son hijos de body
    hijos = driver.find_elements_by_xpath("/html/body/*") # No nos importa el nombre del elto en concreto
    print("####################print(element.tag_name)##################")
    for element in hijos:
        print(element.tag_name)

    divs = driver.find_elements_by_xpath("/html/body/*/div")
    print(len(divs))

    # COMPONENTE . El punto indica que el camino sigue desde la posicion actual
    divs = body.find_elements_by_xpath("./*/div")
    print(len(divs))

    # COMPONENTE // Salta varios niveles (cuantos valores div son descendientes de body
    divs = driver.find_elements_by_xpath("/html/body//div")
    print(len(divs))
    labels = driver.find_elements_by_xpath("//label")
    print(len(labels))

    id = "ctl00_Contenido_tblInmueble"
    div = driver.find_element_by_id(id)
    label = div.find_element_by_xpath("//label")
    print(label.text)

    # FILTROS [...]
    # Permiten indicar condiciones adicionales que deben cumplir los elementos seleccionados
    # Que tipo de finca le corresponde esta referencia catastral
    e = driver.find_elements_by_xpath("(//label)[position()=1]")
    # A pesar de ser solo uno, recibimos un WebElement
    # OJO XPath tiene como primer elemento el 1, no el 0
    print("####################print(e[0].text)####################")
    print(e[0].text)

    e = driver.find_elements_by_xpath("(//label)[1]")
    print(e[0].text)

    # Cuando hayamos terminado de usar Selenium convene cerrar el driver para liberar recursos
    driver.close()


lat, lon = devuelve_coordenadas()
print('LATITUD:', lat, 'LONGITUD', lon)

catastro(lat,lon)