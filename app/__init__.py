from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Lock
import numpy as np
import math

from models import Agent, RadiusAngleTiler
from services import d, angle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


episode = 0
episodes = 10
steps = 100
game_thread = None
coyote_thread = None
road_runner_thread = None
thread_lock = Lock()

stage_height = 500
stage_width = 500
track_radius = 150
step = 0
go = True
capture_distance = 35

roadRunner_initial_position = (stage_width/4, stage_height/4)
coyote_initial_position = (stage_width/2, stage_height/2)

roadRunner = Agent(name="Road Runner"
   , xpos=roadRunner_initial_position[0], ypos=roadRunner_initial_position[1], speed=5)
coyote = Agent(name="Coyote"
   , xpos=coyote_initial_position[0], ypos=coyote_initial_position[1], speed=1)

jose = models.RadiusAngleTiler(r_min=0, r_max=500, nbins=7)

"""
def update_road_runner():
    global go
    global step
    global steps
    global episode
    global episodes
    while episode <= episodes:
        socketio.sleep(0.05)
        roadRunner.xpos = track_radius * math.cos( 2 * step/360. * math.pi) + stage_width / 2
        roadRunner.ypos = track_radius * math.sin( 2 * step/360. * math.pi) + stage_height / 2
        socketio.emit('road_runner_position', {"xpos": roadRunner.xpos, "ypos": roadRunner.ypos}, namespace='/chase')
        step += 1
        if step > steps:
            go = False
            episode += 1
            reset()
"""

def update_players():
    global go
    global step
    global steps
    global episode
    global episodes
    while episode <= episodes:
        r = d(roadRunner, coyote)
        a = angle(roadRunner, coyote)
        f = jose.feature_vec(a=a, r=r)
        socketio.sleep(0.05)

        c = roadRunner.chooseAction(jose.abins)
        if c < len(jose.abins):
            roadRunner.moveAlong(jose.abins[c][1])
        coyote.moveTo(roadRunner)

        socketio.emit('road_runner_position', {"xpos": roadRunner.xpos, "ypos": roadRunner.ypos}, namespace='/chase')
        socketio.emit('coyote_position', {"xpos": coyote.xpos, "ypos": coyote.ypos}, namespace='/chase')
        step += 1
        if step > steps or r <= capture_distance:
            episode +=1
            reset()


"""
def update_coyote():
    global go
    global episode
    global episodes
    while episode <= episodes:
        socketio.sleep(0.05)
        newx, newy = coyote.moveTo(roadRunner)
        coyote.xpos = newx
        coyote.ypos = newy
        socketio.emit('coyote_position', {"xpos": coyote.xpos, "ypos": coyote.ypos}, namespace='/chase')
        if d(coyote, roadRunner) <= 30:
            socketio.emit('episode_end', namespace='/chase')
            go = False
            episode += 1
            reset()
"""

def reset():
    global go
    global step
    global episode
    socketio.emit('episode_end',data={"step": step, "episode":episode}, namespace='/chase')
    roadRunner.xpos = roadRunner_initial_position[0]
    roadRunner.ypos = roadRunner_initial_position[1]
    socketio.emit('road_runner_position', {"xpos": roadRunner.xpos, "ypos": roadRunner.ypos}, namespace='/chase')
    coyote.xpos = coyote_initial_position[0]
    coyote.ypos = coyote_initial_position[1]
    socketio.emit('coyote_position', {"xpos": coyote.xpos, "ypos": coyote.ypos}, namespace='/chase')
    print("episode %s ended at step %s" % (episode, step))
    go = True
    step = 0

@app.route('/')
def index():
    print("in index")
    return render_template('index.html'
    , stage_height=stage_height, stage_width=stage_width
    , roadRunner=roadRunner, coyote=coyote)

@socketio.on('connect', namespace='/chase')
def test_connect():
    print("connected, I think")
    global game_thread
    with thread_lock:
        if game_thread is None:
            game_thread = socketio.start_background_task(target=update_players)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
