import requests
import csv
import matplotlib.pyplot as plt
import os
import os.path

save_path = os.path.abspath(os.getcwd()) + '/data'
completeName = os.path.join(save_path, '10-02-2020_00:00:00_datos.txt')  


# MOSTRAREMOS GRÁFICAMENTE LA EVOLUCIÓN DE LA CONTAMINACIÓN POR ÓXIDO DE NITRÓGENO, HOY EN LA PLAZA DE ESPAÑA
# Abrimos fichero
with open(completeName) as csvfile:
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


