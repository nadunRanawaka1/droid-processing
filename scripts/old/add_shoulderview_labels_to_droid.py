import h5py
import pickle
from copy import deepcopy
import nexusformat.nexus as nx
import time

metadata_fp = "/coc/flash8/wshin49/droid/metadata/all_droid_metadata_with_camera_angles.pkl"

with open(metadata_fp, "rb") as f:
    metadata = pickle.load(f)

droid_fn = "/nethome/nkra3/8flash/Droid_backup/droid_hdf5/droid.hdf5"
droid = h5py.File(droid_fn, 'a')
droid_data = droid['data']

processed = 0
start = time.time()

for index, row in metadata.iterrows():

    if (processed % 100) == 0:
        print(f"Processed demos: {processed}. Time elasped: {time.time() - start}")
    processed += 1

    demo_num = row['Demo']
    
    demo = droid_data[demo_num]

    if 'shoulderview_left_image' in demo['obs']:
        del demo['obs/shoulderview_left_image']
    if 'shoulderview_right_image' in demo['obs']:
        del demo['obs/shoulderview_right_image']

    cam1_side = row['camera1']
    if cam1_side == 'left':
        demo['obs/shoulderview_left_image'] = demo['obs/exterior_image_1_left']
        demo['obs/shoulderview_right_image'] = demo['obs/exterior_image_2_left']

    elif cam1_side == 'right':
        demo['obs/shoulderview_left_image'] = demo['obs/exterior_image_2_left']
        demo['obs/shoulderview_right_image'] = demo['obs/exterior_image_1_left']

    
droid.close()

# droid = nx.nxload(droid_fn)
# print(droid.tree)