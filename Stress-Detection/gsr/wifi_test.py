from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received from Arduino:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
