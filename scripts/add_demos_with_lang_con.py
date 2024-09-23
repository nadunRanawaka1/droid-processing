import pickle
from robomimic.utils.file_utils import create_hdf5_filter_key

metadata_fp = "/media/nadun/Data/Droid/metadata/droid_metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"

with open(metadata_fp, "rb") as f:
    df = pickle.load(f)

filtered_df = df[df['language_instruction_1'].str.strip() != '']

demos = filtered_df['Demo'].tolist()
filter_key = "successful_with_lang"
droid_path = ""

ep_lengths = create_hdf5_filter_key(droid_path, demos, filter_key)


print()