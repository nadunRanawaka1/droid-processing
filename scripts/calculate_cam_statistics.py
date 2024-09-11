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

def calculate_cam_statistics(metadata_path, filter_z=False):
    """
    This function can calculate statistics for pick and place locations for demos in a metadata file.
    :param metadata_path: path to metadata file which is a pandas dataframe stored as a pickle
    :param filter_z: whether to filter out demos where the pick z locations are far from the base of the robot.
    :return: a dictionary containing the stats
    """
    # Read in metadata
    df = pd.read_pickle(metadata_path)

    shoulderview_left_extrinsics = []
    shoulderview_right_extrinsics = []
    for index, row in df.iterrows():
        cam1_side = row['camera1']
        if cam1_side == 'left':
            # cam 1 is on the left
            shoulderview_left_extrinsics.append(row['ext1_cam_extrinsics'])
            shoulderview_right_extrinsics.append(row['ext2_cam_extrinsics'])
        elif cam1_side == 'right':
            # cam 1 is on the right
            shoulderview_right_extrinsics.append(row['ext1_cam_extrinsics'])
            shoulderview_left_extrinsics.append(row['ext2_cam_extrinsics'])
        else:
            raise Exception("Got incorrect label for camera")

    shoulderview_left_extrinsics = np.array(shoulderview_left_extrinsics)
    shoulderview_right_extrinsics = np.array(shoulderview_right_extrinsics)


    ### Calculate some statistics for the spatial locations of the cameras (in robot base frame)
    mean_left_extrinsics = np.mean(shoulderview_left_extrinsics, axis=0)
    std_left_extrinsics = np.std(shoulderview_left_extrinsics, axis=0)

    mean_right_extrinsics = np.mean(shoulderview_right_extrinsics, axis=0)
    std_right_extrinsics = np.std(shoulderview_right_extrinsics, axis=0)





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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()


    parser.add_argument("--metadata_path",
                        type=str,
                        # required=True,
                        default=None,
                        help="path to droid metadata file to calculate statistics for")

    args = parser.parse_args()

    if args.metadata_path is None:
        cam_stats = calculate_cam_statistics(metadata_path)
        raise Exception("Pass in a metadata path for Droid demos")


    if args.metadata_path is not None:
        droid_stats = calculate_cam_statistics(args.metadata_path)
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