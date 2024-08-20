from robomimic.utils.file_utils import create_hdf5_filter_key
import pickle
import h5py

dataset_file_path = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/place_bowl_on_plate/place_bowl_on_plate_vary_both_locations_big_demo.hdf5"

dataset_file = h5py.File(dataset_file_path)
demos = dataset_file['data']
demo_names = demos.keys()

filter_keys_to_list_of_demos = {
    'pick_place_large_spatial' : list(demo_names),
    'pick_place_small_spatial' : list(demo_names)
}

dataset_file.close()

for filter_key in filter_keys_to_list_of_demos:
    demo_keys = filter_keys_to_list_of_demos[filter_key]
    ep_lengths = create_hdf5_filter_key(dataset_file_path, demo_keys, filter_key)
    print(ep_lengths)

