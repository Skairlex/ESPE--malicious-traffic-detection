from datetime import datetime
from mail_sender import sendMail

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

    def create_data_table(menu,analisisMenu,tipo,interfaces,list_table):
        data={
        'menu': menu,
        'analisisMenu': analisisMenu,
        'tipo': tipo,
        'interfaces': interfaces,
        'param':list_table
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
    
    def create_data_atack(atacks):
        count=0
        count_dos=0
        for i in range(len(atacks)):
            if atacks[i].tipo=='Web Attack Brute Force':
                count+=1
            if atacks[i].tipo=='DOS Atack':
                count_dos+=1
        data = list()

        for i in range(len(atacks)):
            print('imors')
            print(atacks[i])
            print(atacks[i].tipo)
            print(count)
            if atacks[i].tipo=='Web Attack Brute Force' and count>5:
                data.append(
                    {
                        "puerto_origen": atacks[i].puerto_origen, 
                        "puerto_destino": atacks[i].puerto_destino, 
                        "fecha": atacks[i].fecha,
                        "ip_origen":atacks[i].ip_origen,
                        "ip_destino":atacks[i].ip_destino,
                        "tipo":atacks[i].tipo
                    }
                )
            elif atacks[i].tipo=='DOS Atack'and count_dos>5:
                data.append(
                    {
                        "puerto_origen": atacks[i].puerto_origen, 
                        "puerto_destino": atacks[i].puerto_destino, 
                        "fecha": atacks[i].fecha,
                        "ip_origen":atacks[i].ip_origen,
                        "ip_destino":atacks[i].ip_destino,
                        "tipo":atacks[i].tipo
                    }
                )
            elif atacks[i].tipo=='Web Attack XSS':
                data.append(
                    {
                        "puerto_origen": atacks[i].puerto_origen, 
                        "puerto_destino": atacks[i].puerto_destino, 
                        "fecha": atacks[i].fecha,
                        "ip_origen":atacks[i].ip_origen,
                        "ip_destino":atacks[i].ip_destino,
                        "tipo":atacks[i].tipo
                    }
                )
        #print('puertos: ',puertos)
        return data

    def send_email(list_atack,mail):
        if(len(list_atack)<1):
            return False
        else:
            count_force=0
            count_dos=0
            count_other=0
            for i in range(len(list_atack)):
                if(list_atack[i]['tipo']=='Web Attack Brute Force'):
                    count_force+=1
                elif(list_atack[i]['tipo']=='DOS Atack'):
                    count_dos+=1
                else:
                    count_other+=1
            if(count_force>10 or count_dos>10 or count_other>0 ):
               sendMail(mail)
               return True
        return False

    def convert_analisis_to_list(analisis):
        list_analisis = list()
        for i in analisis:
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
        
    def convert_parameters_to_list(analisis):
            list_parameter = list()
            for i in analisis:
                list_parameter.append(
                    {
                        'id' : i.id, 
                        'nombre' : i.nombre,
                        'descripcion':i.descripcion,
                        'valor': i.valor,
                    }
                )
            return list_parameter

    def format_parameter(parameter):
        return  {
                    'id' : parameter.id, 
                    'nombre' : parameter.nombre,
                    'descripcion':parameter.descripcion,
                    'valor': parameter.valor,
                }  
            
