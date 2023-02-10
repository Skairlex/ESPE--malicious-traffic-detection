from flask import Flask,render_template,request,redirect,url_for,flash
from readingAlgorithm.readingAlgorith import predict
from flowRecorder import watchInterface,run_by_web
from celery_config import make_celery
from celery import result
from celery.contrib.abortable import AbortableTask

from celery.task.control import revoke
from app_functions import App_functions

from flask_sqlalchemy import SQLAlchemy

from random import choice

import os

from sqlalchemy.sql import func



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from time import sleep

from billiard.exceptions import Terminated

from datetime import datetime


from models import Results,Escaner,Bitacora,Base,Analisis


#Conexion SQLAlchemy para Celery
app= Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='db+mysql://root:root@localhost:3306/analizer'

#Conexion SQLAlchemy para App
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/analizerAlchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key='mysecretkey'

celery=make_celery(app)
db = SQLAlchemy(app)

engine = create_engine('mysql://root:root@localhost:3306/analizerAlchemy')

Session = sessionmaker(engine)
session = Session()


#PAGINA PRINCIPAL
@app.route('/')
def index():
    data={'tipo':2,
    'dato': "interfaces"
    }
    return render_template('index.html',data=data)


# MENU OPCIONES
@app.route('/menu/<menuNav>/<analisisMenu>')
def menu_inicio(menuNav,analisisMenu):
    
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    print ("Seleccion de menu .........")
    print(menuOp)
  
    if menuOp==4:
        print(menuOp)
        list_analisis=get_list_analisis()
        print(list_analisis)
        data=App_functions.create_data_analisis(menuOp,analisisOp,1,'',list_analisis)
        #data=App_functions.create_data_menu(menuOp,analisisOp,1,'')
    else:
        data=App_functions.create_data_menu(menuOp,analisisOp,1,'')
    
    flash(data)
    return redirect(url_for('index'))
    

#BOTON INICIAR
@app.route('/reviewInterfaces/<menuNav>/<analisisMenu>',methods=['POST'])
def method_name(menuNav,analisisMenu):
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    interfaces=watchInterface()
    puertos = App_functions.convert_interfaces(interfaces)
    data=App_functions.create_data_menu(menuOp,analisisOp,1,puertos)
    flash(data)
    return redirect(url_for('index'))


#Background process happening without any refreshing
#INTERFACE SELECTED
@app.route('/background_process_test/<param>/<menuNav>/<analisisMenu>')
def background_process_test(param,menuNav,analisisMenu):
    puerto = int(format(param))
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    interfaces=watchInterface()
    data_interfaces=App_functions.get_data_interfaces(puerto,interfaces)
    crearRegistros()
    result=listen_flow.delay((int(puerto)))
    #print(result.state)
    #print(result)
    crear_datos_analisis(result.id)
    data=App_functions.create_data_task(menuOp,analisisOp,1,data_interfaces['interfaces'],result.id,data_interfaces['puerto'])
    flash(data)
    return redirect(url_for('index'))




#REVOCA PROCESO EN RABBITMQ
@app.route('/cancelar/<task_id>/<menuNav>/<analisisMenu>/<terminal>')
def cancelar(task_id, menuNav, analisisMenu, terminal):
    print("ID Tarea: ",task_id)
    #task = reverse.AsyncResult(task_id)
    #task.abort()
    tarea = format(task_id)
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))

    interfaces=watchInterface()
    puertos=App_functions.convert_interfaces(interfaces)

    revoke(task_id, terminate=True)

    data_analisis = get_data_analisis()
    observations = App_functions.get_observations(data_analisis)
    update_analisis(task_id,observations['result'])
    
    #result=crearRegistrosBitacora.delay(format(terminal))

    #crearRegistrosBitacora("terminal")

    fecha = datetime.now()
    fechaText = fecha.date()

    print("FECHA ACTUAL:  ",fechaText)
    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos,
        'task': tarea,
        'paquetes': observations['num_paquetes'],
        'fecha':fechaText,
        'analisis':data_analisis
        
            
    }

    flash(data)

    return redirect(url_for('index'))

def update_analisis(task_id,result):
    analisis = session.query(Analisis).filter(Analisis.task_id == task_id).first()
    analisis.fechaFin=App_functions.get_date()
    analisis.resultado=result
    analisis.estado='Finalizado'
    session.add(analisis)
    session.commit()


def get_data_analisis():
    dato_1 = session.query(Escaner).filter(Escaner.id == 1).first()
    dato_2 = session.query(Escaner).filter(Escaner.id == 2).first()
    dato_3 = session.query(Escaner).filter(Escaner.id == 3).first()
    dato_4 = session.query(Escaner).filter(Escaner.id == 4).first()

    paquetes = dato_1.cantidad + dato_2.cantidad + dato_3.cantidad + dato_4.cantidad
    analisis=[
            {
                "tipo": dato_1.tipo,
                "nombre": dato_1.nombre,
                "Cantidad": dato_1.cantidad
            },
            {
                "tipo": dato_2.tipo,
                "nombre": dato_2.nombre,
                "Cantidad": 0 if dato_2.cantidad<20 else dato_2.cantidad
            },
            {
                "tipo": dato_3.tipo,
                "nombre": dato_3.nombre,
                "Cantidad": dato_3.cantidad
            },
            {
                "tipo": dato_4.tipo,
                "nombre": dato_4.nombre,
                "Cantidad": dato_4.cantidad
            },
        ]
    return analisis

def get_list_analisis():
    resp = session.query(Analisis).all()
    list_analisis = list()
    for i in resp:
        list_analisis.append(
            {
                'id' : i.id, 
                'fechaInicio' : i.fechaInicio[0:16],
                'fechaFin':'-' if i.fechaFin is None else i.fechaFin[0:16],
                'resultado': i.resultado,
                'task_id':i.task_id,
                'estado':i.estado
            }
        )
    return list_analisis


def insertarDatos():
    insert.delay()
    return 'DATOS INCERTADOS.....'
    #return insert()

@celery.task(name='celery_example.listen_flow')
def listen_flow(num):
    #return string
    #update_state(state='PROGRESS')
    run_by_web(num)
    return redirect(url_for('index'))

@celery.task(name='celery_example.reverse')
def reverse(string):
    print("PENSANDO...")
    #sleep(10)
    #return string
    print("FIN...")
    print(string)
    return string[::-1]

@celery.task(name='celery_example.insertar')
def insert():
    print("PASO 1")
    for i in range(100):
        data = ''.join(choice('ABCDE') for i in range(10))
        result = Results(data=data)
        session.add(result)

    session.commit()

    return 'Datos insertado alchemy....'

@celery.task(name='celery_example.crearRegistrosBitacora')
def crearRegistrosBitacora(terminal):
    print("REGISTROS BASE")

    fecha = datetime.now()
    fechaText = fecha.date()
    
    dato_1 = session.query(Escaner).filter(Escaner.id == 1).first()
    dato_2 = session.query(Escaner).filter(Escaner.id == 2).first()
    dato_3 = session.query(Escaner).filter(Escaner.id == 3).first()
    dato_4 = session.query(Escaner).filter(Escaner.id == 4).first()

    registro = Bitacora(
    terminal=terminal, 
    fecha=fechaText, 
    beningn =               dato_1.cantidad, 
    attack_brute_force =    dato_2.cantidad, 
    attack_XSS =            dato_3.cantidad,
    attack_SQL_injection =  dato_4.cantidad)

    session.add(registro)

    session.commit()

    return 'Nuevo registro bitacora ingresado...'


#CREAR REGISTROS BASE PARA CONTEO DE PAQUETES
def crearRegistros():
    print("REGISTROS BASE")
    atacks=session.query(Escaner).all()
    print(atacks)
    if len(atacks)==0: 
        print('Creacion ataques en base')
        dato_1 = Escaner(tipo=1, nombre="Benigno",                  cantidad=0)
        dato_2 = Escaner(tipo=2, nombre="Web Attack Brute Force",   cantidad=0)
        dato_3 = Escaner(tipo=3, nombre="Web Attack XSS",           cantidad=0)
        dato_4 = Escaner(tipo=4, nombre="Web Attack SQL injection", cantidad=0)
        session.add(dato_1)
        session.add(dato_2)
        session.add(dato_3)
        session.add(dato_4)
    else:
        print('Encerando ataques en base')
        for atack in atacks:
            atack.cantidad=0
    session.commit()
    return 'Datos creados alchemy....'


#CREAR REGISTROS PARA BITACORA
def crear_datos_analisis(task_id):
    fecha=App_functions.get_date()
    #time_stamp = time.time()
    #fechaText = datetime.fromtimestamp(time_stamp)
    analisis = Analisis(fechaInicio=fecha, resultado="Protegido",task_id=task_id,estado='Ejecutandose')
    session.add(analisis)
    session.commit()


def actualizar():
    print("REGISTROS ACTUALIZADO")
    dato = session.query(Escaner).filter(Escaner.id == 3).first()
    dato.cantidad = 8
    session.commit()

    return 'Datos actualizados alchemy....'

def buscarTipo(tipo):
    #print("BUSCAR")
    dato = session.query(Escaner).filter(Escaner.id == tipo).first()
    print(dato.cantidad)

    return dato.cantidad

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "Ok"

def pagina_no_encontrada(error):
    #return render_template("404.html"),404
    return redirect(url_for('index'))

if __name__=='__main__':
    #Conectar y crear registro base
    
    #actualizar()
    #buscarTipo(1)
    #buscarTipo(2)
    #buscarTipo(3)
    #buscarTipo(4)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Base created...')
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True,port=5000)

    

    

