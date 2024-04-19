from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer, KafkaConsumer
import json
from databaseConnection import conexionBD

class procesamiento_eventos:
    def __init__(self, data):
        self.data = data
    
    def procesar_pipeline(self):
        """ Funcion para procesar los eventos de tipo pipeline que llegan desde Azure
        Args:     
        json: diccionario con
            event: nombre del evento procesado (pipeline), con este valor se sabe a cual tabla de la base de datos ingresar la información
            data: diccionario con las columnas y valores que se insertan en la base de datos
        """
        job = self.data.get('resource', {}).get('job', {})
        if job:
            # Extracción de datos del job
            job_id = job.get('id')
            job_name = job.get('name')
            job_state = job.get('state')
            job_result = job.get('result')
            start_time = job.get('startTime')
            finish_time = job.get('finishTime')

            return {
                'event': 'pipeline',
                'job_id': job_id,
                'job_name': job_name,
                'job_state': job_state,
                'job_result': job_result,
                'start_time': start_time,
                'finish_time': finish_time
            }
        else:
            return "Información de job no disponible"
    
    def procesar_commit(self):
        """ Funcion para procesar los eventos de tipo commit que llegan desde Azure
        Args:     
        json: diccionario con
            event: nombre del evento procesado (commit), con este valor se sabe a cual tabla de la base de datos ingresar la información
            data: diccionario con las columnas y valores que se insertan en la base de datos
        """
        commit = self.data.get('resource', {}).get('commits', {})
        if commit:
            commit_id = commit.get('commitId')
            commit_author = commit.get('author',{}).get('email')
            commit_date = commit.get('author',{}).get('date')
            
            return {
                'event': 'commit',
                'commit_id': commit_id,
                'commit_author': commit_author,
                'commit_date': commit_date,
            }
        else:
            return "Información de commit no disponible"
    
    def procesar_PR(self):
        """ Funcion para procesar los eventos de tipo commit que llegan desde Azure
        Args:     
        json: diccionario con
            event: nombre del evento procesado (Pull Request), con este valor se sabe a cual tabla de la base de datos ingresar la información
            data: diccionario con las columnas y valores que se insertan en la base de datos
        """
        pr_info = self.data.get('resource', {})
        if pr_info:
            pr_id = pr_info.get('pullRequestId')
            pr_status = pr_info.get('status')
            if pr_status == 'active':
                pr_date = pr_info.get('creationDate')
            elif pr_status == 'complete':
                pr_date = pr_info.get('closedDate')

            return {
                'event': 'PR', 
                'data' : {
                'pr_id': pr_id,
                'pr_status': pr_status,
                'pr_date': pr_date}
            }
        else:
            return "Información de Pull Request no disponible"
    
    
    def obtener_tipo_evento(self):
        """ Funcion para que obtiene el tipo de evento de la plataforma Azure, esta función identifica si es une vento relevante para el sistema
        y llama a la función correspondiente al tipo de evento encontrado (commit, pipeline o PR)
        Args:     
        json: diccionario con
            info: diccionario con las columnas y valores de acuerdo al evento determinado
        """
        publisherId = self.data.get('publisherId')
        if 'pipelines' in publisherId:
            info = self.procesar_pipeline()
            return info
        if 'tfs' in publisherId:
            eventType = self.data.get('eventType')
            if 'pullrequest' in eventType:
                info =self.procesar_PR()
                return info
            else:
                info = self.procesar_commit()
                return info

    def procesar_evento_azure(self):
        """ Funcion para que originalmente llama al evento, por ahora solo se tiene configurado el procesamiento de evento para Azure,
        queda pendiente definición si llamar todos los eventos aqui o tener una función para procesar el evento de cada plataforma
        Args:     
        str: Cadena de conexión retornando un procesamiento exitoso
        """
        event= self.obtener_tipo_evento()
        tipoEvento = event['event']

        data = event['data']
        conexion = conexionBD()
        columnas = list(data.keys())
        valores = list(data.values())
        insertar = conexion.insertBD(tipoEvento, columnas, valores)
    
        return "Evento de Azure DevOps procesado"
    
    
    
    
    
    
    
    
    
    
    
    
    def procesar_evento_github(self):
        print("Procesando evento de GitHub...")
        return "Evento de GitHub procesado"
    
    def procesar_evento_gitlab(self, data):
        print("Procesando evento de GitLab...")
        return "Evento de GitLab procesado"