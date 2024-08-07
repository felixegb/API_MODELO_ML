from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json


app = FastAPI()

class model_input (BaseModel):
    pFrontRight: float
    pFrontLeft: float
    pBackRight: float 
    pBackLeft: float
    oilLevel: float 
    breaksLevel: float
    gasLevel: float 
    refrigerant: float

# Cargar el modelo
modelo_sensors = pickle.load(open('modelo_pre.sav', 'rb'))
resultado = None

@app.post('/mantenimiento')
def mantenimiento_pre(parametros: model_input):
    global resultado
    entrada = parametros.json()
    entrada_dicc = json.loads(entrada)
    
    pFR = entrada_dicc['pFrontRight']
    pFL = entrada_dicc['pFrontLeft']
    pBR = entrada_dicc['pBackRight']
    pBL = entrada_dicc['pBackLeft']
    oL = entrada_dicc['oilLevel']
    bL = entrada_dicc['breaksLevel']
    gL = entrada_dicc['gasLevel']
    refri = entrada_dicc['refrigerant']
    
    entrada_lista = [pFR, pFL, pBR, pBL, oL, bL, gL, refri]
    predict = modelo_sensors.predict([entrada_lista])
    
    resultado = 'Su automóvil no necesita mantenimiento' if predict[0] == 0 else 'Su automóvil necesita mantenimiento, consulte a su mecánico'
    return resultado

@app.get('/prueba')
def prueba ():
    if resultado is not None:
        return resultado
    else:
        return 'No hay resultados disponibles'
