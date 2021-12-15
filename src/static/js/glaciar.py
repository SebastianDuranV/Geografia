from datetime import date
from datetime import datetime
from koboextractor import KoboExtractor
import pandas as pd

# Obtener los datos de la base de datos de internet
KOBO_TOKEN = '26566dd7934bcb45fee86851765c4f7c867e9cc3'
kobo = KoboExtractor(KOBO_TOKEN, 'https://kf.kobotoolbox.org/api/v2') # kobo.humanitarianresponse.info
asset_uid = "atX9jThsvhvhhjFf573eng" #"a7Wd6TUVqejWxSwBkzSGY9"
#today = date.today()
#datos_today = kobo.get_data(asset_uid,submitted_after = today )
data = kobo.get_data(asset_uid)
data = data['results']

puntos = ["punto_1", "punto_2", "punto_3", "punto_4", "punto_5" , "punto_6"]

# Obtener las imagenes
def getUrlData(punto,data):
    lista_data_i = []
    #lista_name = []
    for i in range (len(data)):
        if data[i]['Punto_de_Observaci_n'] == punto:
            lista_data_i.append(data[i])
            #lista_name.append(data[i][])

    return lista_data_i[:5] #, lista_name[:5]

def getCountryData(punto,data):
    list_data = []
    





