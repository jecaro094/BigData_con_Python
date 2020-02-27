from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import os.path
import time
import requests
import csv


def generate_plot(completeName):

    with open(completeName) as csvfile:
        # Dictionary hours-gass emissions levels
        dict_levels={}
        # Generamos vector con los valores separados por coma
        readCSV = csv.reader(csvfile, delimiter=',')
        plazaEspaña = '28079008'
        oxidoNitrogeno = '12'
        for row in readCSV:
            if (row[0] + row[1] + row[2] == plazaEspaña and row[3] == oxidoNitrogeno):
                hora = 0
                desp = 9
                vs = []
                horas = []
                while hora <= 23:
                    if row[desp + 2 * hora + 1] == 'V':
                        vs.append(int(row[desp + 2 * hora]))
                        horas.append(hora)
                        dict_levels.update( {hora : int(row[desp + 2 * hora])} )
                    hora += 1

        return dict_levels

def get_files(folder_name):
    save_path = os.path.abspath(os.getcwd()) + f'/{folder_name}'
    files_list = [f for f in os.listdir(save_path) if f.endswith("datos.txt")]
    return files_list

def job():

    # NOTE Carpeta en la que guardaré los datos
    if not os.path.exists('data'):
        os.makedirs('data')

    # NOTE Here, I'll store all dictionaries from every single txt file
    dictionary_sum = {}
    dictionary_mean = []
    counter_key = {}

    # NOTE Página web de la que hago scraping
    url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    resp = requests.get(url) # Response 200 (status_code la página se descargó con éxito)

    # NOTE Creo path en el que se encuentran los ficheros con los datos semanales
    save_path = os.path.abspath(os.getcwd()) + '/data'

    # NOTE Defino dataframe con los valores de las emisiones para cada día
    horas = range(0,25)
    df = pd.DataFrame(columns=horas)
    average_df = pd.DataFrame(columns=horas)

    # PLOT / Getting dictionary for each txt file
    for index, textFile in enumerate(get_files('data')):
        completeName = os.path.join(save_path, textFile)  
        dictionary_file = generate_plot(completeName)
        df.loc[textFile] = pd.Series(dictionary_file)

    # NOTE Media de las emisiones de gases
    df.loc['media'] = pd.Series(df.mean())
    
    ax = plt.gca()
    df.iloc[0:-2].T.plot(kind='line',legend=True,ax=ax)
    df.iloc[-1].T.plot(kind='line',lw=3, color='black',y='media',legend=True, ax=ax)
    plt.show()

  

job()
