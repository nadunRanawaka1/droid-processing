"""
This script can be used to calculate the pick and place location statistics for a .hdf5 file or from pandas dataframe
"""

import pandas as pd
import numpy as np
import pickle
import h5py
import time
from utils import get_action_info_rl2
import argparse


metadata_path = "/media/nadun/Data/Droid/metadata/droid_metadata/can_demos_with_colors.pkl"
demo_path = "/media/nadun/Data/Droid/datasets/kitchen/retriever/can/put_green_can_in_box_small_bounding_box_demo.hdf5"

def stats_from_metadata(metadata_path, filter_z=False):
    """
    This function can calculate statistics for pick and place locations for demos in a metadata file.
    :param metadata_path: path to metadata file which is a pandas dataframe stored as a pickle
    :param filter_z: whether to filter out demos where the pick z locations are far from the base of the robot.
    :return: a dictionary containing the stats
    """
    # Read in metadata
    df = pd.read_pickle(metadata_path)

    # Next we pick demos that have only one pick and place action
    only_single_picks = df[df['num_gripper_closes'] == 1]
    pick_locations = only_single_picks['pick_locations'].tolist()
    pick_locations_array = np.concatenate(pick_locations)[:, 0:3]

    # Next we filter the demos based on the z location because we want demos
    # that have a z location close to the base of the robot (OPTIONAL)
    if filter_z:
        z_locations = pick_locations_array[:, 2]
        z_mask = np.logical_and(z_locations >= -0.05, z_locations <= 0.20)
        only_single_picks = only_single_picks[z_mask]

    pick_locations = only_single_picks['pick_locations'].tolist()

    ### Calculate some statistics for the spatial locations of the pick actions
    pick_locations_array = np.concatenate(pick_locations)[:, 0:3]
    mean_pick_locations = np.mean(pick_locations_array, axis=0)
    std_pick_locations = np.std(pick_locations_array, axis=0)

    ### Now calculate statistics for the place locations

    place_locations = only_single_picks['place_locations'].tolist()
    place_locations_array = np.concatenate(place_locations)[:, 0:3]
    mean_place_locations = np.mean(place_locations_array, axis=0)
    std_place_locations = np.std(place_locations_array, axis=0)


    # What demos did we actually use to calculate the statistics?
    demos_used_for_statistics = only_single_picks['Demo'].tolist()
    stats = {"pick_mean": mean_pick_locations,
             "pick_std": std_pick_locations,
             "place_mean": mean_place_locations,
             "place_std": std_place_locations,
             "demos": demos_used_for_statistics
    }
    return stats

def stats_from_dataset(demo_path):
    demo_file = h5py.File(demo_path)
    demos = demo_file["data"]

    num_gripper_closes_per_demo = []
    num_gripper_opens_per_demo = []
    gripper_open_times_per_demo = []  # when in the demo the gripper opened (from closed state)
    gripper_close_time_per_demo = []

    pick_locations_per_demo = []
    place_locations_per_demo = []
    pick_time_per_demo = []
    place_time_per_demo = []

    num_demos = 0
    demo_nums = []

    start = time.time()

    for demo in demos:
        demo_nums.append(demo)

        # if (num_demos % 10) == 0:
        #     print(f"Processing demo: {num_demos} . Time elapsed: {time.time() - start}")

        num_demos += 1
        demo = demos[demo]

        ### Get gripper opens and closes, and based on that pick and place action info
        (gripper_opens, gripper_closes, gripper_open_times, gripper_close_times,
         pick_times, place_times, pick_locations, place_locations) = get_action_info_rl2(demo)

        # TODO maybe filter demos by if they have more than 1 gripper close/open

        num_gripper_opens_per_demo.append(gripper_opens)
        num_gripper_closes_per_demo.append(gripper_closes)
        gripper_open_times_per_demo.append(gripper_open_times)
        gripper_close_time_per_demo.append(gripper_close_times)


        pick_time_per_demo.append(pick_times)
        place_time_per_demo.append(place_times)
        pick_locations_per_demo.append(pick_locations)
        place_locations_per_demo.append(place_locations)

    ### First we calculate statistics for the pick locations
    pick_locations_array = np.concatenate(pick_locations_per_demo)[:, 0:3]

    # Calculate some statistics for the spatial locations of the actions
    mean_pick_locations = np.mean(pick_locations_array, axis=0)
    std_pick_locations = np.std(pick_locations_array, axis=0)

    ### Next calculate statistics for the place locations
    place_locations_array = np.concatenate(place_locations_per_demo)[:, 0:3]
    mean_place_locations = np.mean(place_locations_array, axis=0)
    std_place_locations = np.std(place_locations_array, axis=0)

    stats = {"pick_mean": mean_pick_locations,
             "pick_std": std_pick_locations,
             "place_mean": mean_place_locations,
             "place_std": std_place_locations,
             "demos": demo_nums
             }
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_path",
                        type=str,
                        # required=True,
                        default=None,
                        help="path to rl2 dataset to calculate statistics for")
    parser.add_argument("--metadata_path",
                        type=str,
                        # required=True,
                        default=None,
                        help="path to droid metadata file to calculate statistics for")

    args = parser.parse_args()

    if args.dataset_path is None and args.metadata_path is None:
        raise Exception("Pass in either a hdf5 path for an RL2 dataset or a metadata path for Droid demos")

    if args.dataset_path is not None:
        rl2_stats = stats_from_dataset(args.dataset_path)
        print(f"Stats for rl2 demo dataset: ")
        print("================================================================================")

        print(f"Pick mean: {rl2_stats['pick_mean']}")
        print(f"Pick std dev: {rl2_stats['pick_std']}")
        print(f"Place mean: {rl2_stats['place_mean']}")
        print(f"Place std dev: {rl2_stats['place_std']}")

        print("================================================================================")

    if args.metadata_path is not None:
        droid_stats = stats_from_metadata(args.metadata_path)
        print(f"Stats for droid demos:")

        print("================================================================================")

        print(f"Pick mean: {droid_stats['pick_mean']}")
        print(f"Pick std dev: {droid_stats['pick_std']}")
        print(f"Place mean: {droid_stats['place_mean']}")
        print(f"Place std dev: {droid_stats['place_std']}")
        print("================================================================================")

        print(f"Demos used for stats: {droid_stats['demos']}")

        print("================================================================================")



print()