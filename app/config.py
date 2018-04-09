import math

stage_height = 500
stage_width = 800
track_radius = 150

episodes = 10
steps = 100


lmbda = 0.6
learning_interval = 10

radius_min = 0
radius_max = math.sqrt(stage_height**2 + stage_width**2)
radius_bins = 7
angle_min = -math.pi
angle_max = math.pi
angle_bins = 7
state_space_dims = radius_bins + angle_bins

action_space_dims = angle_bins + 1 # includes None action

roadRunner_speed = 50
coyote_speed = 5
capture_distance = 35
capture_penalty = -10
escape_reward = 100
