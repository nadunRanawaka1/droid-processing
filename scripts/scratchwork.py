import pickle
import nexusformat.nexus as nx
import h5py
import random
import re
import pandas as pd

metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/new_droid_metadata.pkl"

df = pd.read_pickle(metadata_fp)

# unique_lang_1_counts = df["language_instruction_1"].value_counts()[1:] # index from 1 to remove empty string
# unique_lang_2_counts = df["language_instruction_2"].value_counts()[1:]
# unique_lang_3_counts = df["language_instruction_3"].value_counts()[1:]

print()

### RANDOM SCRATCHWORK
