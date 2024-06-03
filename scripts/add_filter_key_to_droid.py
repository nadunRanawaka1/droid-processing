from robomimic.utils.file_utils import create_hdf5_filter_key
import pickle

droid_file_path = "/nethome/nkra3/flash7/Droid/droid_hdf5/droid.hdf5"

filter_keys_to_list_of_demos_file_path = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/droid_filter_dict_pick_location_in_and_ood_target_place_bowl.pkl" #pickle file

f = open(filter_keys_to_list_of_demos_file_path, 'rb')
filter_keys_to_list_of_demos = pickle.load(f)

for filter_key in filter_keys_to_list_of_demos:
    demo_keys = filter_keys_to_list_of_demos[filter_key]
    ep_lengths = create_hdf5_filter_key(droid_file_path, demo_keys, filter_key)
    print(ep_lengths)

f.close()