import math

stage_height = 500
stage_width = 800
track_radius = 150

episodes = 20
steps = 100


lmbda = 0.6
learning_interval = 7

radius_min = 0
radius_max = math.sqrt(stage_height**2 + stage_width**2)
radius_bins = 7
angle_min = -math.pi
angle_max = math.pi
angle_bins = 7
state_space_dims = radius_bins + angle_bins

action_space_dims = angle_bins + 1 # includes None action

roadRunner_speed = 50
coyote_speed = 15
capture_distance = 35
movement_penalty = -1
capture_penalty = -100
escape_reward = 100
memory_capacity = 500
learning_epsilon = 0.01
learning_eta = 0.01
greedy_epsilon = 0.05
