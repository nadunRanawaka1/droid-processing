import pickle
import nexusformat.nexus as nx
import h5py
import random
import re
import pandas as pd

metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/droid_metadata.pkl"

df = pd.read_pickle(metadata_fp)



unique_lang_1_counts = df["language_instruction_1"].value_counts()[1:] # index from 1 to remove empty string
unique_lang_2_counts = df["language_instruction_2"].value_counts()[1:]
unique_lang_3_counts = df["language_instruction_3"].value_counts()[1:]

top_5_lang_1 = unique_lang_1_counts[:5]


lang_1_to_demos = {}

for index, value in top_5_lang_1.items():
    selected = df[df['language_instruction_1'] == index]
    lang_1_to_demos[index] = selected["Demo"].values.tolist()

print()

with open("/media/nadun/Data/Droid/droid-processing/droid_filter_keys/lang_1_to_demos.pkl", "wb") as f:
    pickle.dump(lang_1_to_demos, f)

### RANDOM SCRATCHWORK
