from datetime import datetime
import os
import os.path
import schedule
import time
import requests

def job():

    # NOTE Carpeta en la que guardaré los datos
    if not os.path.exists('data'):
        os.makedirs('data')

    # NOTE Página web de la que hago scraping
    url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    resp = requests.get(url) # Response 200 (status_code la página se descargó con éxito)

    # NOTE Creo paths y archivo con los datos
    save_path = os.path.abspath(os.getcwd()) + '/data'
    now = datetime.now()
    textFile = now.strftime(f"%d-%m-%Y_%H:%M:%S_datos.txt")
    completeName = os.path.join(save_path, textFile)  
    
    with open(completeName, 'wb') as output:
        output.write(resp.content)

    # NOTE Mensaje a la salida 'datos_salida.txt'
    message = f'FICHERO CREADO: {textFile}'     
    finalMessage = now.strftime(f"RESP={resp} DAY=[%d/%m/%Y] HOUR=[%H:%M:%S] {message} ")
    print(finalMessage)	

# NOTE Mirar en 'programacion.py' para definir cada cuánto quiero que se ejecute "job"   
#schedule.every().minute.at(":00").do(job)
#schedule.every().hour.at(":52:59").do(job)
schedule.every().day.at("17:55:59").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

