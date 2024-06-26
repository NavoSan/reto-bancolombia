from flask import Flask, request, jsonify, render_template
from rutas import main 
from kafka import KafkaProducer, KafkaConsumer
import json
from controller import procesamiento_eventos
import logging



app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


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
        send_event_to_kafka('github-events', data)

        procesamiento_eventos.procesar_evento_github(data)

        return jsonify({'status': 'Received GitHub events',}), 200
    
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
        send_event_to_kafka('azure-events', data)

        procesamiento_eventos.procesar_evento_azure(data)

        return jsonify({'status': 'Received Azure event'}), 200 #, 'respuesta':respuesta}), 200
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
        send_event_to_kafka('gitlab-events', data)

        procesamiento_eventos.procesar_evento_gitlab(data)

        return jsonify({'status': 'Received GitLab event'}), 200 #, 'respuesta':respuesta}), 200
    except Exception as e:
        print(e)
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
@app.route('/webhook-status')
def webhook_status():
    return render_template('webhook_status.html', message=last_request_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
