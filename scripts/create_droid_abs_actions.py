import h5py
import numpy as np
import argparse

def droid_to_real_format(droid_path):

    droid = h5py.File(droid_path, 'a')

    droid_data = droid['data']
    processed = 0
    for demo_name in droid_data:

        if (processed % 1000) == 0:
            print(f"Processed demo : {processed}")
        processed += 1
        demo = droid_data[demo_name]

        # Creating absolute action
        ee_action = demo['cartesian_position_action'][:]
        gripper_action = demo['gripper_position_action'][:]
        gripper_action_copy = np.copy(gripper_action)
        gripper_action_copy[gripper_action_copy < 0.5] = -1.0
        gripper_action_copy[gripper_action_copy >= 0.5] = 0.0
        absolute_action = np.concatenate((ee_action, gripper_action_copy), axis=1)
        droid_data.create_dataset(f'{demo_name}/absolute_actions', data=absolute_action)

    droid.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--droid_path",
                        type=str,
                        required=True,
                        help="path to droid")

    args = parser.parse_args()

    droid_to_real_format(args.droid_path)
