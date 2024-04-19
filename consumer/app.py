from flask import Flask, jsonify, render_template
from rutas import main
from kafka import KafkaConsumer
import json

app = Flask(__name__)
app.register_blueprint(main)

consumer = KafkaConsumer(
    'github-events',
    'azure-events',
    'gitlab-events',
    bootstrap_servers='kafka:29092',
    auto_offset_reset='earliest',
    group_id='my-group-id',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

@app.route('/consume', methods=['GET'])
def consume():
    messages = []
    try:
        # Consume messages
        for message in consumer:
            messages.append({
                'topic': message.topic,
                'message': message.value
            })
            # Solo para demostración, podrías querer tener un control más sofisticado
            if len(messages) >= 10:  # Limita a 10 mensajes para no atascar el endpoint
                break
        return render_template('consume.html', messages=messages)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Registro del Blueprint del archivo rutas.py



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8890, debug=True)