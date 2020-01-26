import json
import tweepy

CONSUMER_TOKEN = "nnsdHKtE0uzfYTMMYhPYSBc0z"
CONSUMER_SECRET = "6c9eZs1h6zLHuS7l6ukrP33juWD8FZzHU9zOlF1UhgJwSab0v2"
ACCESS_TOKEN = "74711111-Z6XmD8OzL2fpxHzd1JGkLRJqKTzP1yuboTlQiT5Ff"
ACCESS_SECRET = "2DG8rKqwtvusGNljmEPs1fcoDPJdiYuI6bh6d6Jswr9Ah"
# creamos una autenticacion (objeto de la clase OAuthHandler) para usar la API
auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
# Introducimos nuestros tokens de acceso
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
# Creamos el objeto API para hacer consultas
api = tweepy.API(auth)

# Descargando Tweets ya almacenados con search
lista_tweets = api.search(q="python")
lista_json = []
for tweet in lista_tweets:
    lista_json.append(tweet._json)

print(len(lista_json))
print(lista_json[0])

# Busqueda de Tweets en Streaming
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, ruta):
        super().__init__(api)
        self.fich = open(ruta, 'a')

    def on_status(self, status):
        self.fich.write(json.dumps(status._json) + "\n")

    def on_error(selfself, status_code):
        self.fich.close()

ruta_datos = "./datos_twitter.txt"
myStreamListener = MyStreamListener(api, ruta_datos)
flujo = tweepy.Stream(auth = auth, listener=myStreamListener)

flujo.filter(track=['python'])
