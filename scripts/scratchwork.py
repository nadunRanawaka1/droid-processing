import pickle
import nexusformat.nexus as nx
import h5py
import random
import re
import pandas as pd

# metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/droid_metadata.pkl"
metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/all_droid_metadata.pkl"
# metadata_fp = "/media/nadun/Data/Droid/metadata/droid_metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"
#
# df = pd.read_pickle(metadata_fp)

# # unique_lang_1_counts = df["language_instruction_1"].value_counts()[1:] # index from 1 to remove empty string
# # unique_lang_2_counts = df["language_instruction_2"].value_counts()[1:]
# # unique_lang_3_counts = df["language_instruction_3"].value_counts()[1:]

# search_strings = ["cube", "block"]

# cube_mask = df['language_instruction_1'].str.contains('|'.join(search_strings), case=False) | df['language_instruction_2'].str.contains('|'.join(search_strings), case=False) | df['language_instruction_3'].str.contains('|'.join(search_strings), case=False)

# df = df[cube_mask]

# cube_demos = {}
# cube_demos["demos_with_cubes"] = df["Demo"].values.tolist()

# with open("/media/nadun/Data/Droid/droid-processing/droid_filter_keys/cube_demos_list.pkl", "wb") as f:
#     pickle.dump(cube_demos, f)

# print()
print()

### RANDOM SCRATCHWORK

# fp = "/media/nadun/Data/Droid/metadata/droid_metadata/all_droid_metadata_with_colors.pkl"

# with open(fp, "rb") as f:
#     metadata = pickle.load(f)

demo_fn = "/nethome/nkra3/robomimic-v2/datasets/retriever/put_marker_in_cup/target_datasets/30_target_dataset.hdf5"
demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

# demo_file = h5py.File(demo_fn, 'r')
# masks = demo_file['mask']
# print(masks['successful_with_lang'][:])

# demos = demo_file['data']
# demo = demos['demo_20']

# eef_pos = demo['obs/eef_pos'][:]
# absolute_actions = demo['absolute_actions'][:]




print()


