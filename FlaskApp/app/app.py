from flask import Flask,render_template,request,redirect,url_for,flash
from readingAlgorithm.readingAlgorith import predict
from flowRecorder import watchInterface,run_by_web
from celery_config import make_celery
from celery import result
from celery.contrib.abortable import AbortableTask

from celery.task.control import revoke


from flask_sqlalchemy import SQLAlchemy

from random import choice

import os

from sqlalchemy.sql import func

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from time import sleep

from billiard.exceptions import Terminated

#import jsonpickle

app= Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='db+mysql://root:root@localhost:3306/analizer'

#Conexion SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/analizerAlchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key='mysecretkey'

celery=make_celery(app)
db = SQLAlchemy(app)

engine = create_engine('mysql://root:root@localhost:3306/analizerAlchemy')
Base = declarative_base()
BaseEjemplo = declarative_base()

Session = sessionmaker(engine)
session = Session()

#res = result.AsyncResult(job_id)

class Results(BaseEjemplo):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.firstname

class Escaner(Base):
    __tablename__ = 'escaner'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.nombre


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.String(50))

    

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

@app.route('/')
def index():
    #return "<h1>Hola Mundo</h1>"
    cursos=['PHP','Python','Django','Java']
    data1={'titulo':'index',
    'bienvenida': 'Saludos',
    'cursos':cursos,
    'numero_cursos':len(cursos)
    }
    data={'tipo':2,
    'dato': "interfaces"
    }
    return render_template('index.html',data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):
    data= {
        'titulo':'Contacto',
        'nombre': nombre,
        'edad':edad
    }
    return render_template('contacto.html',data=data)

# MENU OPCIONES
@app.route('/menu/<menuNav>/<analisisMenu>')
def menu_inicio(menuNav,analisisMenu):
    
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    print ("Inicio .........")
    #predict()
    interfaces=watchInterface()

    puertos = list()
    for i in range(len(interfaces)):
        puertos.append(
            {
                "id": i, 
                "dato": interfaces[i]
            }
        )

    print('puertos: ',puertos)

    print('len: ',len(interfaces))

    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos
    }

    flash(data)
    print("bye")
    return redirect(url_for('index'))
    

@app.route('/reviewInterfaces/<menuNav>/<analisisMenu>',methods=['POST'])
def method_name(menuNav,analisisMenu):
    print ("Hello .........")
    #predict()

    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))
    print ("Inicio .........")
    #predict()
    interfaces=watchInterface()

    puertos = list()
    for i in range(len(interfaces)):
        puertos.append(
            {
                "id": i, 
                "dato": interfaces[i]
            }
        )

    print('puertos: ',puertos)

    print('len: ',len(interfaces))

    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos
    }

    flash(data)
    print("bye")
    return redirect(url_for('index'))

#background process happening without any refreshing
@app.route('/background_process_test/<param>/<menuNav>/<analisisMenu>')
def background_process_test(param,menuNav,analisisMenu):
    #predict()
    #param = request.arg.get('params1','SIN PARAMETROS')

    puerto = int(format(param))
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))

    interfaces=watchInterface()

    puertos = list()
    for i in range(len(interfaces)):
        puertos.append(
            {
                "id": i, 
                "dato": interfaces[i]
            }
        )

    print('puertos: ',puertos)

    print('len: ',len(interfaces))

    
    
    
    result=listen_flow.delay((int(puerto)))
    #result=listen_flow.delay('john')
    #result.wait()
    print(result.state)
    print(result)
    #print(result.status)
    #print(result.id)
    #print(result.get())

    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos,
        'task': result.id
    }

    #sleep(3)

    #print(result)

    flash(data)

    # return ("nothing")
    return redirect(url_for('index'))

@app.route('/cancelar/<task_id>/<menuNav>/<analisisMenu>')
def cancelar(task_id, menuNav, analisisMenu):
    print("ID Tarea: ",task_id)
    #task = reverse.AsyncResult(task_id)
    #task.abort()

    tarea = format(task_id)
    menuOp = int(format(menuNav))
    analisisOp = int(format(analisisMenu))

    interfaces=watchInterface()

    puertos = list()
    for i in range(len(interfaces)):
        puertos.append(
            {
                "id": i, 
                "dato": interfaces[i]
            }
        )

    print('puertos: ',puertos)

    print('len: ',len(interfaces))

    revoke(task_id, terminate=True)

    dato_1 = session.query(Escaner).filter(Escaner.id == 1).first()
    dato_2 = session.query(Escaner).filter(Escaner.id == 2).first()
    dato_3 = session.query(Escaner).filter(Escaner.id == 3).first()
    dato_4 = session.query(Escaner).filter(Escaner.id == 4).first()

    paquetes = dato_1.cantidad + dato_2.cantidad + dato_3.cantidad + dato_4.cantidad

    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos,
        'task': tarea,
        'paquetes': paquetes,
        'analisis':
        [
            {
                "tipo": dato_1.tipo,
                "nombre": dato_1.nombre,
                "Cantidad": dato_1.cantidad
            },
            {
                "tipo": dato_2.tipo,
                "nombre": dato_2.nombre,
                "Cantidad": dato_2.cantidad
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
            
    }

    flash(data)

    return redirect(url_for('index'))

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
    sleep(10)
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

#@celery.task(name='celery_example.crearRegistros')
def crearRegistros():
    print("REGISTROS BASE")
    dato_1 = Escaner(tipo=1, nombre="Benigno",                  cantidad=0)
    dato_2 = Escaner(tipo=2, nombre="Web Attack Brute Force",   cantidad=0)
    dato_3 = Escaner(tipo=3, nombre="Web Attack XSS",           cantidad=0)
    dato_4 = Escaner(tipo=4, nombre="Web Attack SQL injection", cantidad=0)

    session.add(dato_1)
    session.add(dato_2)
    session.add(dato_3)
    session.add(dato_4)

    session.commit()

    return 'Datos creados alchemy....'

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    crearRegistros()
    #actualizar()
    #buscarTipo(1)
    #buscarTipo(2)
    #buscarTipo(3)
    #buscarTipo(4)
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True,port=5000)

    

