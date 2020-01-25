# Si son muy grandes, no interesa ni grabarlo en disco ni cargarlo completo en memoria
# Procesamiento perezoso (usar la menor info posible)
import requests
from contextlib import closing # permite leer directamente el valor devuelto por requests.get
import csv
import codecs # para leer los strings en formato utf-8
import matplotlib.pyplot as plt

# url donde tenemos el fichero colgado en la web. Datos de las mediciones de calidad del aire de la ciudad de Madrid
url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
path_mac = "/Users/carlosrabazo/PycharmProjects/BigData_Python/Tema2/"
path_win= "C:\\Users\\carlo\\OneDrive - Telefonica\\PycharmProjects\\BigData_Python\\Tema2\\"
nombreFicheroDatos = 'horario.txt'

# resp = requests.get(url)

# with open(path_win + nombreFicheroDatos, 'wb') as output:
#    output.write(resp.content)

# with open(path_win + nombreFicheroDatos) as csvfile:
#    readCSV = csv.reader(csvfile, delimiter=',')

# No lo graba en disco porque lee directamente del request.get() ni lo carga completo en memoria por stream=True
with closing(requests.get(url, stream=True)) as r:
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
    plazaEspaña = '28079008'
    oxidoNitrogeno = '12'
    for row in reader:
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


