### app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from server.realtime_data import start_streaming

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('connect')
def test_connect():
    print("Client connected")

def run_server():
    threading.Thread(target=start_streaming, args=(socketio,), daemon=True).start()
    socketio.run(app, debug=True)

if __name__ == '__main__':
    run_server()
