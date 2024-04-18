from flask import Flask
from rutas import main 

app = Flask(__name__)

# Registro del Blueprint del archivo rutas.py
app.register_blueprint(main)

# Ruta para el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    from flask import request, jsonify
    if request.method == 'POST':
        data = request.json
        print("Webhook received!")
        print(data)  # Aquí procesas la información recibida
        return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
