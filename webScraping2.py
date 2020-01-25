# NAVEGACION RELATIVA
# El anterior tipo de navegación es laborioso, decenas de accesos a atributo children si es una pagina media
# (una por nivel). Cambio en estructura, que modifique un elemento de la ruta, hara el codigo inservible
# Con BeautifulSoup podemos buscar elementos sin tener que explicar la ruta compelta find_all()
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
# NAVEGACION RELATIVA DE mini.html
divs = soup.find_all("div")
print("######################print(divs[0].get_text())#####################")
print(divs[0].get_text())
# Podemos reducir aun mas el codigo con el metodo find que devuelve directamente el primer objeto
print(soup.find("div").get_text())
# Estos metodos siguen dependiendo, aunque en menor medida, de la ruta de los elementos en el arbol
# Que pasa si el creador de la web mete un div delante del primero?
# Reducimos la dependencia de la posicion afinando mas la busqueda con los valores de atributos habituales
# id o class. Entonces hacemos la busqueda independiente de la posicion (de numero de elementos div)
print(soup.find("div", id="date").get_text()) # ESTE ES EL ELEMENTO CLAVE DE HOY
# MIRAR LA DOCUMENTACION DE LA BIBLIOTECA BeautifulSoup que tiene muchas opciones
# select() devuelve todos los elementos descendientes de otro elemento (hijos, hijos de los hijos, etc)
print(soup.select("html div")[0].get_text())
