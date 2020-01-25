import requests
import csv
import matplotlib.pyplot as plt

# url donde tenemos el fichero colgado en la web. Datos de las mediciones de calidad del aire de la ciudad de Madrid
url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
path_mac = "/Users/carlosrabazo/PycharmProjects/BigData_Python/Tema2/"
path_win= "C:\\Users\\carlo\\OneDrive - Telefonica\\PycharmProjects\\BigData_Python\\Tema2\\"
nombreFicheroDatos = 'horario.txt'

# usamos el metodo pedir el fichero .get
resp = requests.get(url)
print(resp) # Response 200 (status_code la página se descargó con éxito)
# https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
# 2xx éxito, 4xx o 5xx error

# Por comodidad grabamos el fichero en el disco local
# Construcción with asegura que se cierre el fichero al finalizar
with open(path_win + nombreFicheroDatos, 'wb') as output:
    output.write(resp.content)

# Colummas 0,1,2 : concatenan la estación - 28079004 es Plaza de España
# Columnas 3,4,5 : valor medido. Si 3 es 12 es óxido de nitrógeno. Los otros dos no los usamos
# Columnas 6,7,8 : año, mes, dia
# Columnas 9-56  : valor de cada hora del día (parejas: valor y si segundo = V -> Valor válido y N -> No tener en cuenta)
# MOSTRAREMOS GRÁFICAMENTE LA EVOLUCIÓN DE LA CONTAMINACIÓN POR ÓXIDO DE NITRÓGENO, HOY EN LA PLAZA DE ESPAÑA
# Abrimos fichero
with open(path_win + nombreFicheroDatos) as csvfile:
    # Generamos vector con los valores separados por coma
    readCSV = csv.reader(csvfile, delimiter=',')
    plazaEspaña = '28079008'
    oxidoNitrogeno = '12'
    for row in readCSV:
        if (row[0] + row[1] + row[2] == plazaEspaña and row[3] == oxidoNitrogeno):
            print(row[0] + row[1] + row[2] + row[3])
            plt.title("Óxido de Nitrógeno: " + row[8] + "/" + row[7] + "/" + row[6])
            hora = 0
            desp = 9
            vs = []
            horas = []
            while hora <= 23:
                if row[desp + 2 * hora + 1] == 'V':
                    vs.append(int(row[desp + 2 * hora]))
                    horas.append(hora)
                hora += 1
            plt.plot(horas, vs)
            plt.show()
            print("Gráfico Mostrado")


