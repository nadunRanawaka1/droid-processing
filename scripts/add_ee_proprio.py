import h5py
import numpy as np
import argparse
import time
import nexusformat.nexus as nx
import tensorflow_graphics.geometry.transformation as tfg
from robomimic.utils.transform_utils import vec2axisangle, axisangle2vec, axisangle2quat


def euler_to_axis_angles(euler):
    axes, angles = tfg.axis_angle.from_euler(euler)
    batch_axis_angles = np.hstack((axes.numpy(), angles.numpy()))
    batch_axis_angles_exp = batch_axis_angles[:, 0:3] * batch_axis_angles[:, 3, np.newaxis]
    return batch_axis_angles_exp


def add_ee_proprio(droid_path):

    droid = h5py.File(droid_path, 'a')

    droid_data = droid['data']
    processed = 0
    start = time.time()
    for demo_name in droid_data:

        if (processed % 1000) == 0:
            print(f"Processed demo : {processed} . Time elapsed: {time.time() - start}")
        processed += 1
        demo = droid_data[demo_name]


        # Transform cartesian pos obs to axis angle
        ee_pose = np.copy(demo['obs/cartesian_position'][:])
        ee_pos = ee_pose[:, 0:3]
        ee_euler = ee_pose[:, 3:]
        ee_axis_angle = euler_to_axis_angles(ee_euler)

        ee_quat_list = []
        for i in range(ee_axis_angle.shape[0]):
            axis, angle = vec2axisangle(ee_axis_angle[i])
            quat = axisangle2quat(axis, angle)
            ee_quat_list.append(quat)

        ee_quat = np.array(ee_quat_list)
        ee_pose = np.concatenate([ee_pos, ee_quat], axis=1)


        demo.create_dataset("obs/eef_pos", data=ee_pos)
        demo.create_dataset("obs/eef_quat", data=ee_quat)
        demo.create_dataset("obs/eef_axis_angle", data=ee_axis_angle)
        demo.create_dataset("obs/eef_pose", data=ee_pose)


    droid.close()

    droid_file = nx.nxload(droid_path)
    print(droid_file.tree)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--droid_path",
                        type=str,
                        required=True,
                        help="path to droid")

    args = parser.parse_args()

    add_ee_proprio(args.droid_path)
