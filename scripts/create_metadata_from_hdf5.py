import h5py
import pandas as pd
import numpy as np
from matplotlib.colors import is_color_like
from statistics import mean
import argparse

GRIPPER_STATE_WINDOW_LENGTH = 10


def get_colors_in_string(string):
    string = string.split()
    colors = []
    for word in string:
        if is_color_like(word):
            colors.append(word)
    return colors


def get_action_info(demo):
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


def create_metadata(demo_path, save_path=None):

    demo_file = h5py.File(demo_path)
    demos = demo_file["data"]

    lang_1_list = []
    lang_2_list = []
    lang_3_list = []

    colors_per_demo = []

    num_actions_per_demo = []

    max_ee_velocity_of_demo = []

    num_gripper_closes_per_demo = []
    num_gripper_opens_per_demo = []
    gripper_open_times_per_demo = [] # when in the demo the gripper opened (from closed state)
    gripper_close_time_per_demo = []


    pick_locations_per_demo = []
    place_locations_per_demo = []
    pick_time_per_demo = []
    place_time_per_demo = []

    num_demos = 0

    for demo in demos:

        if (num_demos % 1000) == 0:
            print(f"Processing demo: {num_demos}")

        num_demos += 1
        demo = demos[demo]

        ### Add language instructions
        lang_1_list.append(demo.attrs["language_instruction_1"])
        lang_2_list.append(demo.attrs["language_instruction_2"])
        lang_3_list.append(demo.attrs["language_instruction_3"])

        ### Parse colors
        colors_in_demo = (get_colors_in_string(demo.attrs["language_instruction_1"]) +
                          get_colors_in_string(demo.attrs["language_instruction_2"]) +
                          get_colors_in_string(demo.attrs["language_instruction_3"]))
        colors_in_demo = list(set(colors_in_demo))
        colors_per_demo.append(colors_in_demo)

        ### Add some basic stuff
        num_actions_per_demo.append(demo["action"][:].shape[0])

        cartesian_velocity_action = np.copy(demo["cartesian_velocity_action"][:])
        cartesian_pos_velocity = cartesian_velocity_action[:,0:3]
        cartesian_pos_velocity = np.sum(np.absolute(cartesian_pos_velocity), axis=1)

        max_ee_velocity_of_demo.append(np.max(cartesian_pos_velocity))

        ### Get gripper opens and closes, and based on that pick and place action info
        (gripper_opens, gripper_closes, gripper_open_times, gripper_close_times,
         pick_times, place_times, pick_locations, place_locations) = get_action_info(demo)

        num_gripper_opens_per_demo.append(gripper_opens)
        num_gripper_closes_per_demo.append(gripper_closes)
        gripper_open_times_per_demo.append(gripper_open_times)
        gripper_close_time_per_demo.append(gripper_close_times)

        pick_time_per_demo.append(pick_times)
        place_time_per_demo.append(place_times)
        pick_locations_per_demo.append(pick_locations)
        place_locations_per_demo.append(place_locations)


    # Turn lists into numpy arrays for easy querying
    # gripper_open_times_per_demo = np.array(gripper_close_time_per_demo, dtype=np.int64)
    # gripper_close_time_per_demo = np.array(gripper_close_time_per_demo, dtype=np.int64)
    # pick_time_per_demo = np.array(pick_time_per_demo, dtype=np.int64)
    # place_time_per_demo = np.array(place_time_per_demo, dtype=np.int64)
    # pick_locations_per_demo = np.array(pick_locations_per_demo, dtype=np.float64)
    # place_locations_per_demo = np.array(place_locations_per_demo, dtype=np.float64)


    ### Make a dataframe with all the info
    demo_nums = range(num_demos)
    data = {"Demo": demo_nums,
            "language_instruction_1": lang_1_list,
            "language_instruction_2": lang_2_list,
            "language_instruction_3": lang_3_list,
            "colors_in_demo": colors_per_demo,
            "num_actions": num_actions_per_demo,
            "max_ee_velocity": max_ee_velocity_of_demo,
            "num_gripper_opens": num_gripper_opens_per_demo,
            "num_gripper_closes": num_gripper_closes_per_demo,
            "gripper_open_timesteps": gripper_open_times_per_demo,
            "gripper_close_timesteps": gripper_close_time_per_demo,
            "pick_skill_timestep_ranges": pick_time_per_demo,
            "place_skill_timestep_ranges": place_time_per_demo,
            "pick_locations": pick_locations_per_demo,
            "place_locations":place_locations_per_demo}
    df = pd.DataFrame(data)
    pick_locations_list = df['pick_locations'].tolist()

    df.to_pickle(save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--droid_path",
                        type=str,
                        # required=True,
                        default="/home/nadun/Data/Droid/droid_hdf5/droid_100.hdf5",
                        help="path to droid")

    parser.add_argument("--save_dir",
                        type=str,
                        # required=True,
                        default='/home/nadun/Data/Droid/droid_hdf5',
                        help="where to save metadata")

    args = parser.parse_args()
    demo_fn = args.droid_path
    save_path = f"{args.save_dir}/droid_metadata.pkl"
    create_metadata(demo_fn, save_path=save_path)

