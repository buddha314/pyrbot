from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Lock
import numpy as np
import math
from config import *

from models import Agent, RadiusAngleTiler, Memory, DM
from services import d, angle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


game_thread = None
coyote_thread = None
road_runner_thread = None
thread_lock = Lock()

episode = 0
step = 0

roadRunner_initial_position = (stage_width/4, stage_height/4)
coyote_initial_position = (stage_width/2, stage_height/2)
jose = models.RadiusAngleTiler(r_min=0, r_max=500, nbins=7)
mike = DM(tiler=jose, action_space_dims=action_space_dims
    , state_space_dims=state_space_dims)


roadRunner = Agent(name="Road Runner"
   , xpos=roadRunner_initial_position[0], ypos=roadRunner_initial_position[1]
   , speed=roadRunner_speed
   , stage_width=stage_width, stage_height=stage_height
   , action_space_dims=action_space_dims, state_space_dims=state_space_dims)
coyote = Agent(name="Coyote"
   , xpos=coyote_initial_position[0], ypos=coyote_initial_position[1]
   , speed=coyote_speed
   , stage_width=stage_width, stage_height=stage_height
   , action_space_dims=action_space_dims, state_space_dims=state_space_dims)


def update_players():
    global step
    global steps
    global episode
    global episodes

    options = mike.present_options(step=step, player=roadRunner, opponent=coyote)

    current_state = options['state']
    current_action = roadRunner.chooseAction(options=options)
    while episode <= episodes:
        socketio.sleep(0.05)
        # mike presents presents options
        options = mike.present_options(
            step=step,
            player=roadRunner,
            opponent=coyote)
        # rr chooses, saves his own state
        choice = roadRunner.chooseAction(options=options)
        m = Memory(episode=episode, step=step
            ,current_state=options['state']
            ,current_action=choice )
        # mike rewards, moved roadRunner and Coyote to new states
        reward = mike.present_update(step=step
            , player=roadRunner # moved by Mike
            , choice=choice
            , npc=coyote) # Coyote is also moved by mike
        m.reward = reward
        m.next_state = mike.get_current_state(player=roadRunner,opponent=coyote)
        # rr makes a memory of the initial state, his action, reward, new state
        roadRunner.addMemory(m)
        socketio.emit('road_runner_position', {"xpos": roadRunner.xpos, "ypos": roadRunner.ypos}, namespace='/chase')
        socketio.emit('coyote_position', {"xpos": coyote.xpos, "ypos": coyote.ypos}, namespace='/chase')
        step += 1
        if (episode + step) % learning_interval == 0:
            print("Sleepy time!")
            roadRunner.update_theta()
        if mike.game_over:
            roadRunner.update_theta()
            episode += 1
            reset()

def reset():
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
    mike.game_over=False
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
