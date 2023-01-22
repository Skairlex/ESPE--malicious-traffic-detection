from flask import Flask,render_template,request,redirect,url_for,flash
from readingAlgorithm.readingAlgorith import predict
from flowRecorder import watchInterface,run_by_web


app= Flask(__name__)

app.secret_key='mysecretkey'


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

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    #predict()
    data={'tipo': 3
    }
    flash(data)
    run_by_web(4)
    return ("nothing")

@app.route('/reviewInterfaces',methods=['POST'])
def method_name():
    print ("Hello .........")
    #predict()
    interfaces=watchInterface()
    print('len: ',len(interfaces))
    data={'tipo': 1,
    'dato': interfaces
    }
    flash(data)
    print("bye")
    return redirect(url_for('index'))

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

