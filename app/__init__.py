from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Lock
import math

from models import Agent
from services import d



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
coyote_thread = None
road_runner_thread = None
thread_lock = Lock()

stage_height = 500
stage_width = 500
track_radius = 150

roadRunner = Agent(name="Road Runner", xpos=stage_width/4, ypos=stage_height/4, speed=1)
coyote = Agent(name="Coyote", xpos=stage_width/2, ypos=stage_height/2, speed=0.1)

go = True

def update_road_runner():
    count = 0
    global go
    while go:
        socketio.sleep(0.05)
        roadRunner.xpos = track_radius * math.cos( 2 * count/360. * math.pi) + stage_width / 2
        roadRunner.ypos = track_radius * math.sin( 2 * count/360. * math.pi) + stage_height / 2
        socketio.emit('road_runner_position', {"xpos": roadRunner.xpos, "ypos": roadRunner.ypos}, namespace='/chase')
        count += 1

def update_coyote():
    count = 0
    global go
    while go:
        socketio.sleep(0.05)
        newx, newy = coyote.moveTo(roadRunner)
        coyote.xpos = newx
        coyote.ypos = newy
        socketio.emit('coyote_position', {"xpos": coyote.xpos, "ypos": coyote.ypos}, namespace='/chase')
        if d(coyote, roadRunner) <= 30:
            print("GOT HIM!")
            socketio.emit('episode_end', namespace='/chase')
            go = False
        count += 1



@app.route('/')
def index():
    print("in index")
    return render_template('index.html'
    , stage_height=stage_height, stage_width=stage_width
    , roadRunner=roadRunner, coyote=coyote)

@socketio.on('connect', namespace='/chase')
def test_connect():
    print("connected, I think")
    global road_runner_thread
    global coyote_thread
    with thread_lock:
        if road_runner_thread is None:
            road_runner_thread = socketio.start_background_task(target=update_road_runner)
        if coyote_thread is None:
            coyote_thread = socketio.start_background_task(target=update_coyote)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
