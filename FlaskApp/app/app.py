#FLASK
from flask import Flask,render_template,request,redirect,url_for,flash

#CELERY
from celery_config import make_celery
from celery import result
from celery.contrib.abortable import AbortableTask
from celery.task.control import revoke

#SOCKET IO
from flask_socketio import SocketIO,send

#SQL ALCHEMY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#EXTERN ARCHIVES
from flowRecorder import watchInterface,run_by_web
from app_functions import App_functions
from readingAlgorithm.readingAlgorith import predict
from models import Results,Escaner,Bitacora,Base,Analisis,Resultado,Parametro
from base_func import crearRegistrosIniciales

#UTILITIES  LIBS
from random import random
from threading import Lock
from datetime import datetime
from random import choice
import os
from time import sleep
#from billiard.exceptions import Terminated






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

#Global vars
thread = None
thread_lock = Lock()
runningThread=True
actual_task_id=0

app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

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
        #print(menuOp)
        query=review_analisis()
        list_analisis=App_functions.convert_analisis_to_list(query)
        print(len(list_analisis))
        data=App_functions.create_data_table(menuOp,analisisOp,1,'',list_analisis)
        print(data)
        #data=App_functions.create_data_menu(menuOp,analisisOp,1,'')
    elif menuOp==5:
        query=review_parameter()
        list_parameter=App_functions.convert_parameters_to_list(query)
        data=App_functions.create_data_table(menuOp,analisisOp,1,'',list_parameter)
    else:
        data=App_functions.create_data_menu(menuOp,analisisOp,1,'')
    
    flash(data)
    return redirect(url_for('index'))

    
# MENU OPCIONES WITH PARAM
@app.route('/menu_param/<menuNav>/<analisisMenu>/<param>')
def menu_inicio_param(menuNav,analisisMenu,param):
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    param=int(format(param))
    if menuOp==5 and analisisOp==2:
        query=review_parameter_by_id(param)
        parameter=App_functions.format_parameter(query)
        data=App_functions.create_data_table(menuOp,analisisOp,1,'',parameter)
        flash(data)
    if menuOp==4 and analisisOp==2:
        query=review_atack_by_id(param)
        parameter=App_functions.create_data_atack(query)
        data=App_functions.create_data_table(menuOp,analisisOp,1,'',parameter)
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

@app.route('/save_parameter/<menuNav>/<analisisMenu>/<id>',methods=['POST'])
def save_parameter(menuNav,analisisMenu,id):
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    idOp=int(format(id))
    if request.method == 'POST':
      result = request.form.to_dict()
      print(result)
      print(idOp)
      edit_parameter(result['description'],result['email'],idOp)
    query=review_parameter()

    list_parameter=App_functions.convert_parameters_to_list(query)
    data=App_functions.create_data_table(menuOp,analisisOp,1,'',list_parameter)
    flash(data)
    return redirect(url_for('index'))


#Background process happening without any refreshing
#COMIENZA LECTURA DE PAQUETES DE INTERFAZ SELECCIONADA
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
    #crear_datos_analisis(result.id)
    global actual_task_id
    actual_task_id=str(result.id)
    data=App_functions.create_data_task(menuOp,analisisOp,1,data_interfaces['interfaces'],result.id,data_interfaces['puerto'])
    flash(data)
    return redirect(url_for('index'))




#REVOCA PROCESO EN RABBITMQ
@app.route('/cancelar/<task_id>/<menuNav>/<analisisMenu>/<terminal>')
def cancelar(task_id, menuNav, analisisMenu, terminal):
    global runningThread
    runningThread=False
    global thread
    thread=None
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







#----------------------------------------------------------------------------------------------
#----------------------------------------   CELERY   ------------------------------------------
#----------------------------------------------------------------------------------------------

@celery.task(name='celery_example.listen_flow')
def listen_flow(num_interface):
    #return string
    #update_state(state='PROGRESS')
    id_task=celery.current_task.request.id
    id_analisis=crear_datos_analisis(str(id_task))
    print('Analisis con Id: ',id_analisis)
    #print('Current id : ',str(id))
    #print(str(id))
    #print('FindedId')
    run_by_web(num_interface,id_analisis,id_task)
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



#----------------------------------------------------------------------------------------------
#----------------------------------------  SQL ALCHEMY  ---------------------------------------
#----------------------------------------------------------------------------------------------

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
        dato_4 = Escaner(tipo=4, nombre="DOS Atack", cantidad=0)
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


def review_analisis():
    return session.query(Analisis).all()

def review_parameter():
    return session.query(Parametro).all()

def review_parameter_by_id(id):
    return session.query(Parametro).filter(Parametro.id==id).first()

#CREAR REGISTROS PARA BITACORA
def crear_datos_analisis(task_id):
    fecha=App_functions.get_date()
    #time_stamp = time.time()
    #fechaText = datetime.fromtimestamp(time_stamp)
    analisis = Analisis(fechaInicio=fecha, resultado="Protegido",task_id=task_id,estado='Ejecutandose')
    session.add(analisis)
    session.commit()
    return analisis.id


def actualizar():
    print("REGISTROS ACTUALIZADO")
    dato = session.query(Escaner).filter(Escaner.id == 3).first()
    dato.cantidad = 8
    session.commit()

    return 'Datos actualizados alchemy....'

def edit_parameter(description,email,id):
    dato = session.query(Parametro).filter(Parametro.id == id).first()
    dato.descripcion=description
    dato.valor=email
    session.commit()

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

def update_analisis(task_id,result):
    analisis = session.query(Analisis).filter(Analisis.task_id == task_id).first()
    analisis.fechaFin=App_functions.get_date()
    analisis.resultado=result
    analisis.estado='Finalizado'
    session.add(analisis)
    session.commit()

def review_atacks(id_atack):
    #print(id_atack)
    dato = session.query(Resultado).filter(Resultado.task_id==id_atack).all()
    session.close()
    print(len(dato))
    return dato

def review_atack_by_id(id_atack):
    #print(id_atack)
    dato = session.query(Resultado).filter(Resultado.analisis_id==id_atack).all()
    session.close()
    print('len',len(dato))
    return dato

def buscar_mail():
    session.close()
    dato = session.query(Parametro).filter(Escaner.id == 1).first()
    return dato.valor


#-------------------------------------------------------------------------------------------------
#---------------------------------------  SOCKET IO  ---------------------------------------------
#-------------------------------------------------------------------------------------------------

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Generating random sensor values")
    global runningThread
    global actual_task_id
    sended_mail=False
    while runningThread:
        print('generating')
        print(actual_task_id)
        data=review_atacks(actual_task_id)
        list_atack=App_functions.create_data_atack(data)
        print('There are:',len(list_atack))
        if sended_mail==False:
            mail=buscar_mail()
            print(mail)
            sended_mail= App_functions.send_email(list_atack,mail)
        socketio.emit('updateSensorData', list_atack )
        socketio.sleep(1)

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    global runningThread
    print('Client connected')
    #print(thread)
    with thread_lock:
        if thread is None:
            runningThread=True
            thread = socketio.start_background_task(background_thread)
        else:
            thread=None
            thread = socketio.start_background_task(background_thread)


"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)





#-------------------------------------------------------------------------------------------------
#-------------------------------------------  MAIN  ----------------------------------------------
#-------------------------------------------------------------------------------------------------

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
    crearRegistrosIniciales()
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True,port=5000)

    

    

