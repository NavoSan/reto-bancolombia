from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer, KafkaConsumer
import json

class procesamiento_eventos:
    def __init__(self):
        consumer = KafkaConsumer(
            'github-events',  # Nombre del tópico de Kafka
            bootstrap_servers=['kafka:29092'],  # Lista de brokers de Kafka
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        # Leer mensajes del tópico
        messages = []
    
        # Coloca un límite en el número de mensajes a consumir por request
        max_messages = 10
        count = 0
        
        for message in consumer:
            messages.append(message.value)
            count += 1
            if count >= max_messages:
                break
        
        # Detiene el consumidor y cierra la conexión
        consumer.close()
        
        # Devuelve todos los mensajes en un formato JSON
        return jsonify({
            'status': 'Received GitHub events',
            'messages': messages
        }), 200
        pass

    
    def procesar_evento_github(self, data):
        print("Procesando evento de GitHub...")
        # Supongamos que queremos registrar el tipo de evento y quién lo envió
        event_type = data.get('action', 'No action specified')
        user = data.get('sender', {}).get('login', 'Unknown user')
        print(f"Evento de GitHub de tipo '{event_type}' enviado por {user}")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de GitHub procesado"
    
    def procesar_evento_gitlab(self, data):
        print("Procesando evento de GitLab...")
        event_type = data.get('object_kind', 'No object kind specified')
        user = data.get('user', {}).get('name', 'Unknown user')
        print(f"Evento de GitLab de tipo '{event_type}' enviado por {user}")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de GitLab procesado"

    def procesar_evento_azure(self, data):
        print("Procesando evento de Azure DevOps...")
        event_type = data.get('eventType', 'No eventType specified')
        resource = data.get('resource', {}).get('commits', [])
        print(f"Evento de Azure DevOps de tipo '{event_type}' con {len(resource)} commits")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de Azure DevOps procesado"