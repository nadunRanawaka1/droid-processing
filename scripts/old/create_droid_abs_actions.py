import h5py
import numpy as np
import argparse
import time
import tensorflow_graphics.geometry.transformation as tfg


def euler_to_axis_angles(euler):
    axes, angles = tfg.axis_angle.from_euler(euler)
    batch_axis_angles = np.hstack((axes.numpy(), angles.numpy()))
    batch_axis_angles_exp = batch_axis_angles[:, 0:3] * batch_axis_angles[:, 3, np.newaxis]
    return batch_axis_angles_exp


def droid_to_real_format(droid_path):

    droid = h5py.File(droid_path, 'a')

    droid_data = droid['data']
    processed = 0
    start = time.time()
    for demo_name in droid_data:

        if (processed % 1000) == 0:
            print(f"Processed demo : {processed} . Time elapsed: {time.time() - start}")
        processed += 1
        demo = droid_data[demo_name]

        # Creating absolute action with rotation in axis angle format
        ee_action = np.copy(demo['cartesian_position_action'][:])
        pos_actions = ee_action[:, 0:3]
        euler_rot_actions = ee_action[:, 3:]
        axis_angle_actions = euler_to_axis_angles(euler_rot_actions)
    

        gripper_action = demo['gripper_position_action'][:]
        gripper_action_copy = np.copy(gripper_action)
        gripper_action_copy[gripper_action_copy < 0.5] = -1.0
        gripper_action_copy[gripper_action_copy >= 0.5] = 1.0
        absolute_action = np.concatenate((pos_actions, axis_angle_actions, gripper_action_copy), axis=1)
        # del droid_data[f'{demo_name}/absolute_actions']
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
