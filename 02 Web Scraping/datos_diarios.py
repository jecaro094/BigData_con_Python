from datetime import datetime
from twilio.rest import Client
from botocore.client import Config
import matplotlib.pyplot as plt
import os
import os.path
import schedule
import time
import requests
import csv
import boto3

client = Client()

# TWILIO CREDENTIALS (I)
phoneNumberTo = os. environ['PHONE_NUMBER_TO'] 
phoneNumberFrom = os. environ['PHONE_NUMBER_FROM'] 

# TWILIO CREDENTIALS (II)
twilioAuthToken = os. environ['TWILIO_AUTH_TOKEN'] 
twilioAccountSID = os. environ['TWILIO_ACCOUNT_SID']

# AWS CREDENTIALS
AWSBucket = os. environ['AWS_BUCKET'] 
AWSAccessKeyID = os. environ['AWS_ACCESS_KEY_ID']
AWSSecretAccessKey= os. environ['AWS_SECRET_ACCESS_KEY'] 

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
    
    with open(completeName, 'wb') as csvfile:
        csvfile.write(resp.content)

    with open(completeName) as csvfile:
        # Generamos vector con los valores separados por coma
        readCSV = csv.reader(csvfile, delimiter=',')
        plazaEspaña = '28079008'
        oxidoNitrogeno = '12'
        for row in readCSV:
            if (row[0] + row[1] + row[2] == plazaEspaña and row[3] == oxidoNitrogeno):
                #print(row[0] + row[1] + row[2] + row[3])
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
                plt.savefig('testplot.png')
                #print("Gráfica guardada como testplot.png")

                # USING AWS FOR UPLOADING
                s3 = boto3.client(
                    's3',
                    region_name='us-east-1',
                    aws_access_key_id=str(AWSAccessKeyID),
                    aws_secret_access_key=str(AWSSecretAccessKey)
                )

            
                with open('testplot.png', 'rb') as data:
                    path = 'testplot.png'
                    file = 'testplot.png'
                    extra_args = {'ContentType': 'image/png','ACL': 'public-read'}
                    s3.upload_file(path, AWSBucket, file, extra_args)

            
                url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': str(AWSBucket),
                    'Key': 'testplot.png'
                }
                )

                # NOTE Mensaje a la salida 'datos_salida.txt'
                message = f'FICHERO CREADO: {textFile}'
                size = os.path.getsize(f'{save_path}/{textFile}')     
                finalMessage = now.strftime(f"RESP={resp} DAY=[%d/%m/%Y] HOUR=[%H:%M:%S] {message} SIZE:{size} ")
                print(finalMessage)	

                # Enviar mensaje de WHATSAPP
                clientW = Client(twilioAccountSID,twilioAuthToken)
                clientW.messages.create(body=now.strftime(f"RESP={resp} DAY=[%d/%m/%Y] HOUR=[%H:%M:%S] {message} SIZE:{size}")
                , from_=phoneNumberFrom, to=phoneNumberTo, media_url=url)


                


# NOTE Mirar en 'programacion.py' para definir cada cuánto quiero que se ejecute "job"   
schedule.every().minute.at(":00").do(job)
#schedule.every().hour.at(":35:00").do(job)
#schedule.every().day.at("16:21:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

