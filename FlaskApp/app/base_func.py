from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Escaner,Resultado
from app_functions import App_functions

engine = create_engine('mysql://root:root@localhost:3306/analizerAlchemy')

Session = sessionmaker(engine)
session = Session()

def buscarTipo(tipo):
    dato = session.query(Escaner).filter(Escaner.id == tipo).first()
    return dato.cantidad

def actualizar(tipo):
    dato = session.query(Escaner).filter(Escaner.id == tipo).first()
    temp = buscarTipo(tipo) + 1
    dato.cantidad = temp
    session.commit()

    #return temp
def add_atack(type,port,date,analisis_id,flow_hash,task_id):
    dato = session.query(Resultado).filter(Resultado.flow_hash == flow_hash).first()
    if dato is None:
        save_data=Resultado(tipo=type,puerto=port,fecha=date,flow_hash=flow_hash,analisis_id=analisis_id,task_id=task_id)
        session.add(save_data)
    else:
        dato.tipo=type
    session.commit()



    
    
    
