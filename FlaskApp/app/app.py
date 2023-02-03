from flask import Flask,render_template,request,redirect,url_for,flash
from readingAlgorithm.readingAlgorith import predict
from flowRecorder import watchInterface,run_by_web
from celery_config import make_celery
from celery import result

from flask import request
#import jsonpickle

app= Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://localhost//'
app.config['CELERY_RESULT_BACKEND']='db+mysql://root:root@localhost:3306/analizer'

app.secret_key='mysecretkey'

celery=make_celery(app)

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

@app.route('/shutdown')
def shutdown():

    # If not logged in, return back to the login page.
    if not session or not session['logged_in']:
        return render_template('index.html')

    # Logged_in, continue...
    sys.exit()
    os.exit(0)
    return

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

    data={
        'menu': menuOp,
        'analisisMenu': analisisOp,
        'tipo': 1,
        'interfaces': puertos
    }
    
    flash(data)
    result=listen_flow.delay((int(puerto)))
    #result=reverse.delay('john')
    #result.wait()
    print(result.state)
    print(result)
    # return ("nothing")
    return redirect(url_for('index'))

@celery.task(name='celery_example.listen_flow')
def listen_flow(num):
    #return string
    #update_state(state='PROGRESS')
    run_by_web(num)
    return 'Do it '

@celery.task(name='celery_example.reverse')
def reverse(string):
    #return string
    print(string)
    return string[::-1]



def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "Ok"

def pagina_no_encontrada(error):
    #return render_template("404.html"),404
    return redirect(url_for('index'))

if __name__=='__main__':
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True,port=5000)

