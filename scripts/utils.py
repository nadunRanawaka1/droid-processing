import numpy as np
from matplotlib.colors import is_color_like
from statistics import mean


### CONSTANTS
GRIPPER_STATE_WINDOW_LENGTH = 15


def get_colors_in_string(string):
    string = string.split()
    colors = []
    for word in string:
        if is_color_like(word):
            colors.append(word)
    return colors

def get_action_info_droid(demo):
    gripper_position_action = demo["gripper_position_action"][:]
    curr_open = gripper_position_action[0] < 0.5 # is gripper currently open
    num_opens, num_closes = 0, 0

    gripper_open_times, gripper_close_times = [], []
    pick_locations, place_locations = [], []
    pick_times, place_times = [], [] # this will be a list of tuples (start of skill, end of skill)

    # we use a window to get gripper state to filter out accidental opens/closes
    gripper_state_window = [gripper_position_action[0][0]] * GRIPPER_STATE_WINDOW_LENGTH

    action_start_time = 0
    i = 1
    while i < gripper_position_action.shape[0]:

        next_action = gripper_position_action[i][0]
        gripper_state_window.pop(0)
        gripper_state_window.append(next_action)
        gripper_act_mean = mean(gripper_state_window)

        if (gripper_act_mean >= 0.5) and (curr_open): # the gripper is currently open and we close it
            num_closes += 1
            close_time = i
            gripper_close_times.append(close_time)
            pick_times.append([action_start_time, close_time]) # when the gripper closes from open, we assume a pick action has happened
            pick_locations.append(demo["obs/cartesian_position"][close_time])
            action_start_time = close_time
            curr_open = ~curr_open
        elif (gripper_act_mean < 0.5) and not(curr_open): # the gripper is currently closed and we open it
            num_opens += 1
            open_time = i
            gripper_open_times.append(open_time)
            place_times.append([action_start_time,open_time]) # when the gripper opens, we assume a place action has happened
            place_locations.append(demo["obs/cartesian_position"][open_time])
            action_start_time = open_time
            curr_open = ~curr_open
        i += 1

    return (num_opens, num_closes,
            np.array(gripper_open_times, dtype=np.int64), np.array(gripper_close_times, dtype=np.int64),
            np.array(pick_times, dtype=np.int64), np.array(place_times, dtype=np.int64),
            np.array(pick_locations), np.array(place_locations))

def get_action_info_rl2(demo):
    gripper_position_action = demo["absolute_actions"][:, -1]
    curr_open = gripper_position_action[0] < 0.5 # is gripper currently open
    num_opens, num_closes = 0, 0

    gripper_open_times, gripper_close_times = [], []
    pick_locations, place_locations = [], []
    pick_times, place_times = [], [] # this will be a list of tuples (start of skill, end of skill)

    # we use a window to get gripper state to filter out accidental opens/closes
    gripper_state_window = [gripper_position_action[0]] * GRIPPER_STATE_WINDOW_LENGTH

    action_start_time = 0
    i = 1
    while i < gripper_position_action.shape[0]:

        next_action = gripper_position_action[i]
        gripper_state_window.pop(0)
        gripper_state_window.append(next_action)
        gripper_act_mean = mean(gripper_state_window)

        if (gripper_act_mean >= 0.5) and (curr_open): # the gripper is currently open and we close it
            num_closes += 1
            close_time = i
            gripper_close_times.append(close_time)
            pick_times.append([action_start_time, close_time]) # when the gripper closes from open, we assume a pick action has happened
            pick_locations.append(demo["obs/eef_pos"][close_time])
            action_start_time = close_time
            curr_open = ~curr_open
        elif (gripper_act_mean < 0.5) and not(curr_open): # the gripper is currently closed and we open it
            num_opens += 1
            open_time = i
            gripper_open_times.append(open_time)
            place_times.append([action_start_time,open_time]) # when the gripper opens, we assume a place action has happened
            place_locations.append(demo["obs/eef_pos"][open_time])
            action_start_time = open_time
            curr_open = ~curr_open
        i += 1

    return (num_opens, num_closes,
            np.array(gripper_open_times, dtype=np.int64), np.array(gripper_close_times, dtype=np.int64),
            np.array(pick_times, dtype=np.int64), np.array(place_times, dtype=np.int64),
            np.array(pick_locations), np.array(place_locations))


def get_pick_and_place_locations(demo, num_gripper_opens, num_gripper_closes):

    if num_gripper_closes == 0 and num_gripper_opens == 0: # Did not pick or place anything this demo
        return [], []

    gripper_position_action = demo["gripper_position_action"][:]
    num_actions = gripper_position_action.shape[0]
    start_open = gripper_position_action[0] < 0.5
    pick_locations = []
    place_locations = []

    pick_times = []
    place_times = []

    # gripper must initially be open to pick up an object, therefore if gripper starts closed, find where it opens
    i = 0
    while i < num_actions and (gripper_position_action[i] > 0.5):
        i += 1
    i += 1

    while num_gripper_opens > 0 or num_gripper_closes > 0: # we may pick up more objects than we place (ex. lift task)
        while i < num_actions:
            next_action = gripper_position_action[i]
            if next_action > 0.5: # we just closed the gripper
                num_gripper_closes -= 1
                pick_locations.append(demo["obs/cartesian_position"][i])
                break
            i += 1

        i += 1
        while i < num_actions: #the gripper is currently closed and now we find where it opens to place the object
            next_action = gripper_position_action[i]
            if next_action < 0.5: # we just opened the gripper
                num_gripper_opens -= 1
                place_locations.append(demo["obs/cartesian_position"][i])
                break
            i += 1

    return pick_locations, place_locations


