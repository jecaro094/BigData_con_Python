from datetime import datetime
from twilio.rest import Client
from botocore.client import Config
import pandas as pd
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
                #print(row[0] + row[1] + row[2] + row[3])
                #plt.title("Óxido de Nitrógeno: " + row[8] + "/" + row[7] + "/" + row[6])
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
                #plt.plot(horas, vs)
                #plt.savefig('testplot.png')
                #plt.show() # For showing figure
                #plt.clf() # For clearing figure
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

    # NOTE Creo paths y archivo con los datos
    save_path = os.path.abspath(os.getcwd()) + '/data'
    now = datetime.now()
    textFile = now.strftime(f"%d-%m-%Y_%H:%M:%S_datos.txt")
    completeName = os.path.join(save_path, textFile)  
    
    # NOTE Creo el fichero txt con los datos diarios y vuelco la respuesta
    with open(completeName, 'wb') as csvfile:
        csvfile.write(resp.content)

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
    #print(df)
    
    ax = plt.gca()
    df.iloc[0:-2].T.plot(kind='line',legend=True,ax=ax)
    df.iloc[-1].T.plot(kind='line',lw=3, color='black',y='media',legend=True, ax=ax)
    plt.show()
    plt.savefig('testplot.png')

       


    # NOTE Salida por pantalla
    whatsapp_message = ''
    whatsapp_message += 'FICHEROS: ' + '\n'
    for fichero in get_files('data'):
        whatsapp_message += str(fichero) + '\n'
    whatsapp_message += '\n'+'SUMA: ' + str(dictionary_sum) + '\n'
    whatsapp_message += '\n'+'APARICIONES: ' + str(counter_key) + '\n'
    whatsapp_message += '\n'+'MEDIA: ' + str([ '%.2f' % elem for elem in dictionary_mean ]) + '\n'
    #print(whatsapp_message)

    #print(dictionary_mean)
        

        #print('\n' + f'FILE: {textFile} ' + '\n' + str(generate_plot(completeName)))
    

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
    
    #clientW = Client(twilioAccountSID,twilioAuthToken)
    #clientW.messages.create(from_=phoneNumberFrom, to=phoneNumberTo, media_url=url)
    

# NOTE Do this because I can only receive messages in less than 24 hours interval
def refresh_whatsapp():
    now = datetime.now()
    # Enviar mensaje de WHATSAPP
    clientW = Client(twilioAccountSID,twilioAuthToken)
    clientW.messages.create(body=f"REFRESHING WHATSAPP TWILIO"
    , from_=phoneNumberFrom, to=phoneNumberTo)
    
    print(f"WHATSAPP REFRESHED" + ' ---- ' + now.strftime(f"DAY=[%d/%m/%Y] HOUR=[%H:%M:%S]"))




# NOTE Mirar en 'programacion.py' para definir cada cuánto quiero que se ejecute "job"   
#schedule.every().minute.at(":00").do(job)
#schedule.every().hour.at(":35:00").do(job)

#schedule.every().day.at("23:58:00").do(job)
#schedule.every().day.at("23:59:30").do(refresh_whatsapp)

#while True:
#    schedule.run_pending()
#    time.sleep(1)


job()
#refresh_whatsapp()
#print(get_files('data'))
