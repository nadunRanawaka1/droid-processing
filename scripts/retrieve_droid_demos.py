import pickle

import pandas as pd
import numpy as np
import h5py
import time

# TODO setup some constants

SPATIAL_MEANS = np.array([0.55, 0.05, 0.25])
SPATIAL_DEVIATIONS = np.array([0.30, 0.30, 0.20])

SHOULDERVIEW_LEFT_SPATIAL_MEANS = np.array([-0.10, 0.35, 0.40])
SHOULDERVIEW_RIGHT_SPATIAL_MEANS = np.array([0.05, -0.45, 0.40])
CAM_DEVIATIONS = np.array([0.30, 0.30, 0.10])

metadata_fp = "/media/nadun/Data/Droid/metadata/droid_metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"
metadata_fp = "/coc/flash8/wshin49/droid/metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"

droid_fp = "/nethome/nkra3/8flash/Droid_backup/droid_hdf5/droid.hdf5"
processed_dataset_fp = \
    "/nethome/nkra3/robomimic-v2/datasets/retriever/wipe_plate/cotraining_datasets/all_wipe_plate.hdf5"



def retrieve_objects(df, objects: list=None):
    """

    :param df:
    :param objects: list of strings
    :return:
    """
    if objects is None:
        return df
    if isinstance(objects, list):
        df = df[df['object'].isin(objects)]
    else:
        raise Exception("objects must be of type list")

    return df


def retrieve_spatial(df):
    low_range = SPATIAL_MEANS - SPATIAL_DEVIATIONS
    high_range = SPATIAL_MEANS + SPATIAL_DEVIATIONS

    pick_locations = df['pick_locations'].tolist()
    pick_locations = np.array(pick_locations).squeeze()[:,:3]

    filter = np.all((pick_locations>=low_range) & (pick_locations <=high_range), axis=1)

    filtered_df = df[filter]
    return filtered_df

def retrieve_cam_pose(df):

    left_low = SHOULDERVIEW_LEFT_SPATIAL_MEANS - CAM_DEVIATIONS
    left_high = SHOULDERVIEW_LEFT_SPATIAL_MEANS + CAM_DEVIATIONS

    right_low = SHOULDERVIEW_RIGHT_SPATIAL_MEANS - CAM_DEVIATIONS
    right_high = SHOULDERVIEW_RIGHT_SPATIAL_MEANS + CAM_DEVIATIONS

    # Filter out demos without cam extrinsics
    df = df[df['ext1_cam_extrinsics'].apply(len) > 0]
    df = df[df['ext2_cam_extrinsics'].apply(len) > 0]

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

    shoulderview_left_extrinsics = np.array(shoulderview_left_extrinsics)[:, :3]
    shoulderview_right_extrinsics = np.array(shoulderview_right_extrinsics)[:, :3]

    left_filter = np.all((shoulderview_left_extrinsics >= left_low) & (shoulderview_left_extrinsics <= left_high), axis=1)
    right_filter = np.all((shoulderview_right_extrinsics >= right_low) & (shoulderview_right_extrinsics <= right_high), axis=1)

    both_filter = left_filter & right_filter

    df = df[both_filter]
    return df

def retrieve_colors(df, colors: list = None):
    if colors is None:
        return df
    if isinstance(colors, list):
        colors = [color.lower() for color in colors]
        df = df[df['color'].str.lower().isin(colors)]
    else:
        raise Exception("colors must of type list")
    return df

def create_retrieved_dataset(df, droid_path, processed_dataset_path):
    demos = df['Demo'].tolist()
    print("Creating processed dataset: ")
    start = time.time()

    with h5py.File(droid_path, 'r') as droid:
        droid_grp = droid['data']
        with h5py.File(processed_dataset_path, 'w') as dataset:
            dataset_grp = dataset.create_group('data')
            num_written = 0
            # Copy over droid
            for demo in demos:
                if (num_written % 10) == 0:
                    print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")
                dataset_grp.copy(droid_grp[demo], f'demo_{num_written}')
                dataset_grp[f'demo_{num_written}'].attrs['original_droid_demo'] = demo

                num_written += 1

    print("COMPLETED CREATING PROCESSED DATASET")

def retrieve_n_random(df, n=100):
    return df.sample(n=n)



with open(metadata_fp, "rb") as f:
    df = pickle.load(f)

### First retrieve the object
df = retrieve_objects(df, ['cup', 'mug'])

### Get pick and place tasks

df = df[df['pick_place'] == True]
# Filter out demos with more than one pick/place
df = df[df['num_gripper_closes'] == 1]



### pick 100 random demos
# df = retrieve_n_random(df, n=100)

### Retrieve spatial
# df = retrieve_spatial(df)

### Retrieve color
# df = retrieve_colors(df, colors=['Green'])

### Then retrieve the campose
# df = retrieve_cam_pose(df)


### Pick upto 100 demos
# df = df if len(df) < 100 else df.sample(n=100)
# print(f"Final df: {df}")

create_retrieved_dataset(df, droid_fp, processed_dataset_fp)
