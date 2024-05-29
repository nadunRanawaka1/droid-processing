import h5py
import pandas as pd
import numpy as np
from matplotlib.colors import is_color_like
from statistics import mean
import argparse
import time
import nexusformat.nexus as nx
import pickle

GRIPPER_STATE_WINDOW_LENGTH = 15





def get_action_info(demo):
    gripper_position_action = demo["obs/gripper_position"][:]
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
            pick_locations.append(demo["obs/ee_pos"][close_time])
            action_start_time = close_time
            curr_open = ~curr_open
        elif (gripper_act_mean < 0.5) and not(curr_open): # the gripper is currently closed and we open it
            num_opens += 1
            open_time = i
            gripper_open_times.append(open_time)
            place_times.append([action_start_time,open_time]) # when the gripper opens, we assume a place action has happened
            place_locations.append(demo["obs/ee_pos"][open_time])
            action_start_time = open_time
            curr_open = ~curr_open
        i += 1

    return (num_opens, num_closes,
            np.array(gripper_open_times, dtype=np.int64), np.array(gripper_close_times, dtype=np.int64),
            np.array(pick_times, dtype=np.int64), np.array(place_times, dtype=np.int64),
            np.array(pick_locations), np.array(place_locations))



demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/place_bowl_on_plate/place_bowl_on_plate_vary_both_locations_big_demo_selected_agentview.hdf5"
demo_file = nx.nxload(demo_fn)

print(demo_file.tree)

demo_file = h5py.File(demo_fn)
demos = demo_file["data"]

all_pick_locations = []
all_place_locations = []

demo_nums = []
gripper_open_times_per_demo = [] # when in the demo the gripper opened (from closed state)
gripper_close_time_per_demo = []


pick_locations_per_demo = []
place_locations_per_demo = []
pick_time_per_demo = []
place_time_per_demo = []


for demo in demos:
    demo_nums.append(demo)

    demo = demos[demo]


    ### Get gripper opens and closes, and based on that pick and place action info
    (gripper_opens, gripper_closes, gripper_open_times, gripper_close_times,
        pick_times, place_times, pick_locations, place_locations) = get_action_info(demo)


    gripper_open_times_per_demo.append(gripper_open_times)
    gripper_close_time_per_demo.append(gripper_close_times)

    pick_time_per_demo.append(pick_times)
    place_time_per_demo.append(place_times)
    pick_locations_per_demo.append(pick_locations)
    place_locations_per_demo.append(place_locations)

    all_pick_locations.append(pick_locations)
    all_place_locations.append(place_locations)

all_pick_locations= np.concatenate(all_pick_locations)
print(all_pick_locations.shape)

mean_pick_locations = np.mean(all_pick_locations, axis=0)
std_pick_locations = np.std(all_pick_locations, axis=0)
print(f" Mean pick locations is : {mean_pick_locations}")

all_place_locations = np.concatenate(all_place_locations)
mean_place_locations = np.mean(all_place_locations, axis=0)
std_place_locations = np.std(all_place_locations, axis=0)
print(f" Mean place locations is {mean_place_locations}")

min_pick_locations = np.min(all_pick_locations, axis=0)
max_pick_locations = np.max(all_pick_locations, axis=0)

print(f" Min pick locations : {min_pick_locations}. Max pick location: {max_pick_locations}")

min_place_locations = np.min(all_place_locations, axis=0)
max_place_locations = np.max(all_place_locations, axis=0)

print(f" Min place locations : {min_place_locations}. Max place location: {max_place_locations}")

metric_dict = {
    "mean_pick_locations": mean_pick_locations,
    "std_pick_locations": std_pick_locations,
    "mean_place_locations": mean_place_locations,
    "std_place_locations": std_place_locations
}


data = {"Demo": demo_nums,
            "gripper_open_timesteps": gripper_open_times_per_demo,
            "gripper_close_timesteps": gripper_close_time_per_demo,
            "pick_skill_timestep_ranges": pick_time_per_demo,
            "place_skill_timestep_ranges": place_time_per_demo,
            "pick_locations": pick_locations_per_demo,
            "place_locations":place_locations_per_demo}
df = pd.DataFrame(data)

df.to_pickle("place_bowl_on_plate_spatial_metrics.pkl")


print(metric_dict)








