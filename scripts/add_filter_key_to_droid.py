from robomimic.utils.file_utils import create_hdf5_filter_key

droid_file_path = ""

filter_keys_to_list_of_demos_file_path = "" #pickle file

for filter_key in filter_keys_to_list_of_demos_file_path:
    demo_keys = filter_keys_to_list_of_demos_file_path[filter_key]
    create_hdf5_filter_key(droid_file_path, demo_keys, filter_key)