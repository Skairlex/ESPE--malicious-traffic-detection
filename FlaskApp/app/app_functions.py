from datetime import datetime

import pytz

class App_functions:
    
    def convert_interfaces(interfaces):
        puertos = list()
        for i in range(len(interfaces)):
            puertos.append(
                {
                    "id": i, 
                    "dato": interfaces[i]
                }
            )
        #print('puertos: ',puertos)
        return puertos
    
    def get_data_interfaces(puerto,interfaces):
        terminal = ""
        puertos = list()
        for i in range(len(interfaces)):
            puertos.append(
                {
                    "id": i, 
                    "dato": interfaces[i]
                }
            )
            if i == puerto:
                terminal = interfaces[i]
        #print('puertos id: ',terminal)
        #print('puertos: ',puertos[puerto].dato)
        #print('len: ',len(interfaces))
        data={
            'interfaces': puertos,
            'puerto': terminal
        }
        return data

    def create_data_menu(menu,analisisMenu,tipo,interfaces):
        data={
        'menu': menu,
        'analisisMenu': analisisMenu,
        'tipo': tipo,
        'interfaces': interfaces
        }
        return data

    def create_data_analisis(menu,analisisMenu,tipo,interfaces,list_analisis):
        data={
        'menu': menu,
        'analisisMenu': analisisMenu,
        'tipo': tipo,
        'interfaces': interfaces,
        'list_analisis':list_analisis
        }
        return data

    def create_data_task(menu,analisisMenu,tipo,interfaces,task,puerto):
        data={
        'menu': menu,
        'analisisMenu': analisisMenu,
        'tipo': tipo,
        'interfaces': interfaces,
        'task': task,
        'puerto': puerto
        }
        return data
    
    def get_date():
        quito = pytz.timezone("America/Guayaquil") 
        fecha = datetime.now(quito)
        return fecha

    def get_observations(data_analisis):
        num_paquetes=data_analisis[0]['Cantidad']+data_analisis[1]['Cantidad']+data_analisis[2]['Cantidad']+data_analisis[3]['Cantidad']
        result='Protegido'
        if(data_analisis[1]['Cantidad']>20 or data_analisis[2]['Cantidad']>1 or data_analisis[3]['Cantidad']>1):
            result='Amenaza detectada'
        observations={
            'num_paquetes':num_paquetes,
            'result':result
        }    
        return observations
