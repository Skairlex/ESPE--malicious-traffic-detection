from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Escaner,Resultado,Parametro,Analisis
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
def add_atack(type,date,analisis_id,flow_hash,task_id,ip_src,ip_dst,tp_src,tp_dst):
    session.begin()
    dato = session.query(Resultado).filter(Resultado.flow_hash == flow_hash).first()
    if dato is None:
        save_data=Resultado(tipo=type,fecha=date,flow_hash=flow_hash,analisis_id=analisis_id,task_id=task_id,ip_origen=ip_src,ip_destino=ip_dst,puerto_origen=tp_src,puerto_destino=tp_dst)
        session.add(save_data)
    else:
        dato.tipo=type
    session.commit()
    session.close()

def crearRegistrosIniciales():
    dato_1 = Parametro(nombre='Email', descripcion="Email remitente para alertas", valor='elisejohn1995@gmail.com')
    session.add(dato_1)
    print('Parametro email creado!!')
    session.commit()









    
    
    
