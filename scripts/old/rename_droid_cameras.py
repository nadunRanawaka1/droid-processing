import h5py
import numpy as np
import argparse
import time

def rename_droid_cameras(droid_path):

    droid = h5py.File(droid_path, 'a')

    droid_data = droid['data']
    processed = 0
    start = time.time()
    for demo_name in droid_data:

        if (processed % 100) == 0:
            print(f"Processed demo : {processed} . Time elapsed: {time.time() - start}")
        processed += 1
        demo = droid_data[demo_name]
        left_shoulder_view = demo['obs/exterior_image_1_left']
        right_shoulder_view = demo['obs/exterior_image_2_left']
        eye_in_hand = demo['obs/wrist_image_left']

        if (f'{demo_name}/obs/shoulderview_left_image' in droid_data):
            del droid_data[f'{demo_name}/obs/shoulderview_left_image']
            del droid_data[f'{demo_name}/obs/shoulderview_right_image']
            del droid_data[f'{demo_name}/obs/eye_in_hand_image']

        droid_data[f'{demo_name}/obs/shoulderview_left_image'] = demo['obs/exterior_image_1_left']
        droid_data[f'{demo_name}/obs/shoulderview_right_image'] = demo['obs/exterior_image_2_left']
        droid_data[f'{demo_name}/obs/eye_in_hand_image'] = demo['obs/wrist_image_left']


        # droid_data.create_dataset(f'{demo_name}/obs/shoulderview_left_image', data=np.copy(left_shoulder_view))
        # droid_data.create_dataset(f'{demo_name}/obs/shoulderview_right_image', data=np.copy(right_shoulder_view))
        # droid_data.create_dataset(f'{demo_name}/obs/eye_in_hand_image', data=np.copy(eye_in_hand))
    
    droid.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--droid_path",
                        type=str,
                        required=True,
                        help="path to droid")

    args = parser.parse_args()

    rename_droid_cameras(args.droid_path)
