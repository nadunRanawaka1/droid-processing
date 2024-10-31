import h5py
import numpy as np

droid_fn = "/media/nadun/Data/Droid/datasets/kitchen/retriever/baking/spatial_retrieved.hdf5"

droid = h5py.File(droid_fn, 'r')

droid_demos = droid['data']

for demo in droid_demos:
    demo_data = droid_demos[demo]
    print(f"processing demo : {demo}")

    obs = demo_data['obs']
    actions = demo_data['absolute_actions'][:]

    assert actions.dtype == np.float64, f"Action for demo {demo} has the wrong datatype: {actions.dtype}"
    assert obs['shoulderview_left_image'].dtype == np.uint8, f"Shoulderview left image for demo {demo} has the wrong datatype : {obs['shoulderview_left_image'].dtype}"
    assert obs['shoulderview_right_image'].dtype == np.uint8, f"Shoulderview right image for demo {demo} has the wrong datatype: {obs['shoulderview_right_image'].dtype}"
    assert obs['eef_pos'].dtype == np.float64, f"eef_pos for demo {demo} has the wrong datatype: {obs['eef_pos'].dtype}"
    assert obs['eef_quat'].dtype == np.float64, f"eef_quat for demo {demo} has the wrong dtype: {obs['eef_quat'].dtype}"
    assert obs['gripper_position'].dtype == np.float64, f"gripper_position for demo {demo} has the wrong dtype: {obs['gripper_position'].dtype}"
    assert obs['language_distilbert'].dtype == np.float16, f"language_distilbert for demo{demo} has the wrong dtype: {obs['language_distilbert'].dtype}"


print("ALL DEMOS HAVE THE CORRECT OBS DATATYPES")