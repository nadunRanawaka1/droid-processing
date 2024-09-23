import pickle
from robomimic.utils.file_utils import create_hdf5_filter_key

# metadata_fp = "/coc/flash8/wshin49/droid/metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"

# with open(metadata_fp, "rb") as f:
#     df = pickle.load(f)

# filtered_df = df[df['language_instruction_1'].str.strip() != '']

with open("/nethome/nkra3/8flash/Droid_backup/metadata/successful_demos_with_lang.pkl", "rb") as f:
    demo_list = pickle.load(f)

filter_key = "successful_with_lang"
droid_path = "/nethome/nkra3/8flash/Droid_backup/droid_hdf5/droid.hdf5"

ep_lengths = create_hdf5_filter_key(droid_path, demo_list, filter_key)
print(ep_lengths)


