from flask import Flask, send_from_directory, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

BOOTSTRAP_SERVERS = 'kafka:29092'
TOPIC_NAME = 'github-events'


@app.route('/')
@cross_origin()
def home():
    return render_template("index.html")

""" Kafka endpoints """


@socketio.on('connect', namespace='/kafka')
def test_connect():
    emit('logs', {'data': 'Connection established'})


@socketio.on('kafkaconsumer', namespace="/kafka")
def kafkaconsumer(message):
    consumer = KafkaConsumer(group_id='consumer-1',
                             bootstrap_servers=BOOTSTRAP_SERVERS)
    tp = TopicPartition(TOPIC_NAME, 0)
    # se registra al topico
    consumer.assign([tp])

    consumer.seek_to_end(tp)
    lastOffset = consumer.position(tp)
    consumer.seek_to_beginning(tp)
    emit('kafkaconsumer1', {'data': ''})
    for message in consumer:
        emit('kafkaconsumer', {'data': message.value.decode('utf-8')})
        if message.offset == lastOffset - 1:
            break
    consumer.close()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8890)