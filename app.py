from flask import Flask, request, jsonify, render_template
from rutas import main 

app = Flask(__name__)

# Registro del Blueprint del archivo rutas.py
app.register_blueprint(main)


last_request_status = "No requests received yet."
# Ruta para el webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    global last_request_status
    try:
        data = request.get_json(force=True)
        last_request_status = f"Last request was successful. Data received: {data}"
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        last_request_status = f"Last request failed. Error: {str(e)}"
        return jsonify({'status': 'error', 'message': str(e)}), 400
@app.route('/webhook-status')
def webhook_status():
    return render_template('webhook_status.html', message=last_request_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8880, debug=True)
