import pandas as pd
import numpy as np

metadata_path = "/media/nadun/Data/Droid/droid_hdf5/droid_metadata.xlsx"
metadata_path = "/home/nadun/Data/Droid/droid_hdf5/droid_100_metadata.pkl"

df = pd.read_pickle(metadata_path)


pick_mask = df['language_instruction_1'].str.contains('pick', case=False) | df['language_instruction_2'].str.contains('pick', case=False) | df['language_instruction_3'].str.contains('pick', case=False)
#
pick_df = df[pick_mask]
only_single_picks = pick_df[pick_df['num_gripper_closes'] == 1]
pick_locations = only_single_picks['pick_locations'].tolist()

print()


print()