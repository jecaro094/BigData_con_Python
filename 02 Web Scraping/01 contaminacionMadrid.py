import requests
import csv
import matplotlib.pyplot as plt
import os
import os.path
import boto3
from botocore.client import Config
from twilio.rest import Client

save_path = os.path.abspath(os.getcwd()) + '/data'

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


completeName = os.path.join(save_path, '10-02-2020_23:59:00_datos.txt')  


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
            plt.savefig('testplot.png')
            print("Gráfica guardada como testplot.png")

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

            # Enviar mensaje de WHATSAPP
            clientW = Client(twilioAccountSID,twilioAuthToken)
            clientW.messages.create(body="Hola mundo", from_=phoneNumberFrom, to=phoneNumberTo, media_url=url)


