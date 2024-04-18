from flask import Flask, request, jsonify, render_template
from rutas import main 
from kafka import KafkaProducer, KafkaConsumer
import json
from modules.controller import procesamiento_eventos

app = Flask(__name__)

# Registro del Blueprint del archivo rutas.py
app.register_blueprint(main)

producer = KafkaProducer(bootstrap_servers='kafka:29092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_event_to_kafka(topic, data):
    producer.send(topic, data)
    producer.flush()


last_request_status = "No requests received yet."
# Ruta para el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    global last_request_status
    try:
        data = request.get_json()
        last_request_status = f"Last request was successful. Data received: {data}"
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(e)
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    try:
        global last_request_status
        data = request.json
        last_request_status = f"Last request was successful. Data received: {data}"
        #respuesta = procesamiento_eventos.procesar_evento_github(data)
        send_event_to_kafka('github-events', data)
        print("se inserta")
        consumer = KafkaConsumer(
            'github-events',  # Nombre del tópico de Kafka
            bootstrap_servers=['kafka:29092'],  # Lista de brokers de Kafka
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='my-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        # Leer mensajes del tópico
        for message in consumer:
            print(f"Received message: {message.value}")
            return jsonify({'status': 'Received GitHub event', 'message':message.value}), 200 #, 'respuesta':respuesta}), 200
    except Exception as e:
        print(e)
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/webhook/azure', methods=['POST'])
def azure_webhook():
    try:
        global last_request_status
        data = request.json
        last_request_status = f"Last request was successful. Data received: {data}"
        #respuesta = procesamiento_eventos.procesar_evento_azure(data)
        send_event_to_kafka('azure-events', data)

        print("se inserta")
        consumer = KafkaConsumer(
            'github-events',  # Nombre del tópico de Kafka
            bootstrap_servers=['kafka:29092'],  # Lista de brokers de Kafka
            auto_offset_reset='earliest',  # Comenzar a leer desde el principio del tópico si no hay offset guardado
            group_id='my-group',  # ID del grupo de consumidores, todos los consumidores con el mismo group_id trabajan juntos
            enable_auto_commit=True,  # Permite que el consumidor guarde automáticamente los offsets
            value_deserializer=lambda x: x.decode('utf-8')  # Deserializar el mensaje de bytes a string
        )
        # Leer mensajes del tópico
        for message in consumer:
            print(f"Received message: {message.value}")

        return jsonify({'status': 'Received GitHub event'}), 200 #, 'respuesta':respuesta}), 200
    except Exception as e:
        print(e)
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/webhook/gitlab', methods=['POST'])
def gitlab_webhook():
    try:
        global last_request_status
        data = request.json
        last_request_status = f"Last request was successful. Data received: {data}"
        #respuesta = procesamiento_eventos.procesar_evento_gitlab(data)
        send_event_to_kafka('gitlab-events', data)
        return jsonify({'status': 'Received GitHub event'}), 200 #, 'respuesta':respuesta}), 200
    except Exception as e:
        print(e)
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/webhook-status')
def webhook_status():
    return render_template('webhook_status.html', message=last_request_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
