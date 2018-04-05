from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Lock
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
road_runner_thread = None
thread_lock = Lock()

stage_height = 500
stage_width = 500
track_radius = 150

def update_road_runner(go=True):
    count = 0;
    while go:
        socketio.sleep(0.05)
        newpos = {}
        newpos["x"] = track_radius * math.cos( 2 * count/360. * math.pi) + stage_width / 2
        newpos["y"] = track_radius * math.sin( 2 * count/360. * math.pi) + stage_height / 2
        socketio.emit('road_runner_position', newpos, namespace='/chase')
        count += 1


@app.route('/')
def index():
    print("in index")
    return render_template('index.html', stage_height=stage_height, stage_width=stage_width)

@socketio.on('connect', namespace='/chase')
def test_connect():
    print("connected, I think")
    global road_runner_thread
    with thread_lock:
        if road_runner_thread is None:
            road_runner_thread = socketio.start_background_task(target=update_road_runner)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
