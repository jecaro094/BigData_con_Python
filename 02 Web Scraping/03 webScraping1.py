from bs4 import BeautifulSoup
url = "C:\\Users\\carlo\\OneDrive - Telefonica\\PycharmProjects\\BigData_Python\\Tema2\\mini.html"
with open(url, "r") as f:
    page = f.read() # Se carga la página como un archivo de texto normal
print("######################print(page)#####################")
print(page)
print("######################print(soup.prettify())#####################")
# Soup contendrá la página como una cadena de
# caracteres en un formato interno estructurado
# Indicamos analizador sintáctico (parser) sencillo.
# Si página más complicada podemos usar "html5lib", aunque de mas lento procesamiento
soup = BeautifulSoup(page, "html.parser")
print(soup.prettify())
# NAVEGACION ABSOLUTA DE mini.html
# Estructura arborea de la página HTML: Raiz, hijos, hermanos
hijosDoc = list(soup.children)
print("##################print([type(item) for item in hijosDoc])#####################")
print([type(item) for item in hijosDoc])
print("##################print(hijosDoc)#######################")
print(hijosDoc)
html=hijosDoc[4]
print("##################print(list(html.children))#######################")
print(list(html.children))
body = list(html.children)[7]
print("##################print(list(body.children))#######################")
print(list(body.children))
divDate = list(body.children)[3]
print("##################print(divDate.get_text())#######################")
print(divDate.get_text())
# Inviable este Tipo de Navegación