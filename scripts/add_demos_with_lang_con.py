import pickle
# from robomimic.utils.file_utils import create_hdf5_filter_key

metadata_fp = "/media/nadun/Data/Droid/metadata/droid_metadata/all_droid_metadata_with_pick_and_place_tasks.pkl"
save_path = "/media/nadun/Data/Droid/metadata/successful_demos_with_lang.pkl"

with open(metadata_fp, "rb") as f:
    df = pickle.load(f)

filtered_df = df[df['language_instruction_1'].str.strip() != '']

demo_list = filtered_df['Demo'].tolist()

with open(save_path, "wb") as f:
    pickle.dump(demo_list, f)

# filter_key = "successful_with_lang"
# droid_path = ""
#
# ep_lengths = create_hdf5_filter_key(droid_path, demos, filter_key)


print()