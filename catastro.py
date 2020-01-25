# Usar Console_shortcut de Anaconda para instalar selenium 'python -m pip install selenium'
# Meter en la variable Path Anaconda3 Anaconda3/Scripts Anaconda3/Library/bin
# Descargar ChromeDriver segun la version de Chrome y meterlo en Anaconda3
from selenium import webdriver
driver = webdriver.Chrome()
# Si no funciona la linea anterior, forzamos desde codigo
# import os
# chromedriver = "C:\\Users\\carlo\\Anaconda3"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(executable_path=chromedriver)
url = "https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx"
driver.get(url)

# Hacer click en un enlace
coord = driver.find_element_by_link_text("COORDENADAS")
coord.click()

# Escribir texto
# Primero nos situamos en la casilla de coordenadas - id="ctl00_Contenido_txtLatitud"
lat=driver.find_element_by_id("ctl00_Contenido_txtLatitud")
lon=driver.find_element_by_id("ctl00_Contenido_txtLongitud")

# Introducimos la latitud y longitud usando send_keys()
latitudCimaTeide = "28.2723368"
longitudCimaTeide = "-16.6600606"
# ##############################################################
from selenium.webdriver.common.action_chains import ActionChains
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(lat).click(lat) # Para provocar el click en la caja y que salte el JavaScript
lat.send_keys(latitudCimaTeide)
ActionChains(driver).move_to_element(lon).click(lon) # Para provocar el click en la caja y que salte el JavaScript
lon.send_keys(longitudCimaTeide)
# ##############################################################
# send_keys puede devolver el error missing 'value' por error de
# compatibilidad entre la version del navegador y la del driver

# Pulsamos botones
datos = driver.find_element_by_id("ctl00_Contenido_btnDatos")
datos.click()
# Tras llamar a click, contenido variable driver ha cambiado a la nueva pagina
# En Selenium, siempre que pulsemos un enlace o un boton estaremos cambiando
# la página accesible desde el driver

# Para volver a la pagina anterior usamos JavaScript ejecutado desde el propio driver
driver.implicitly_wait(10)
driver.execute_script("window.history.go(-1)")
driver.implicitly_wait(10)
driver.execute_script("window.history.go(+1)")

# LOCALIZAR ELEMENTOS
# find_element_by_id() primer elemento
# find_element_by_name()
# find_element_by_class_name()
# find_element_by_xpath()
# find_element_by_link_text()
# find_element_by_partial_link_text()vse busca por el prefijo del texto
# find_element_by_tag_name()
# find_element_by_css_selector()
# generan NoSuchElementException si no lo encuentra
# Los equivalentes en plural (salvo by_id porque solo hay uno) obtiene todos los elementos en una lista

# Para localizar los datos que queremos podríamos usar BeautifulSoup o Selenium con XPath
# XPATH Lenguaje de consulta para obtener info de XML que Selenium usa para navegar por paginas HTML
# https://www.w3schools.com/xml/xpath_intro.asp
# Mas detallado http://www.w3.org/TR/xpath
# COMPONENTE /
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

# Navegadores HeadLess, para que no se vean
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
driver = webdriver.Chrome(chrome_options=chrome_options)