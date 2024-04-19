from flask import Flask, jsonify, render_template
from rutas import main
from kafka import KafkaConsumer
import json
from flask_socketio import SocketIO
from threading import Thread


app = Flask(__name__)
app.register_blueprint(main)
socketio = SocketIO(app)

messages = []

def kafka_consumer():
    consumer = KafkaConsumer(
        'github-events',
        'azure-events',
        'gitlab-events',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id='stream-consumer',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    for message in consumer:
        messages.append(message.value)  # Añade cada mensaje a la lista global
        socketio.emit('new_message', {'data': message.value}, namespace='/stream')


@app.route('/consume', methods=['GET'])
def consume():
    return render_template('consume.html')

@socketio.on('connect', namespace='/stream')
def test_connect():
    app.logger.info("Client connected")

@socketio.on('disconnect', namespace='/stream')
def test_disconnect():
    app.logger.info("Client disconnected")

@app.route('/webhook-status')
def webhook_status():
    return render_template('index.html', message=messages)


def run_kafka_consumer():
    thread = Thread(target=kafka_consumer)
    thread.daemon = True  # Hacer el hilo daemon para que finalice cuando el proceso principal lo haga
    thread.start()

if __name__ == '__main__':
    run_kafka_consumer()
    socketio.run(host='0.0.0.0', port=8890, debug=True)