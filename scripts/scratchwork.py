import pickle
import nexusformat.nexus as nx
import h5py
import random

demo_fn = "/nethome/nkra3/flash7/Droid/droid_hdf5/exp_datasets/pick_place_datasets/droid_1000_demos_small_spatial_diversity_agentview_mix.hdf5"

# pickle_path_1 = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/selected_agent_view_as_left_dict_droid_small_spatial.pkl"
# pickle_path_2 = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/selected_agent_view_as_left_dict_droid_large_spatial.pkl"

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

# demo_file = h5py.File(demo_fn, 'r')

# masks = demo_file['mask']

# small_spatial_demos = masks['pick_place_small_spatial'][:].tolist()
# large_spatial_demos = masks['pick_place_large_spatial'][:].tolist()

# for i, demo in enumerate(small_spatial_demos):
#     small_spatial_demos[i] = str(demo, encoding='utf-8')

# for i, demo in enumerate(large_spatial_demos):
#     large_spatial_demos[i] = str(demo, encoding='utf-8')


# print(small_spatial_demos)
# print("============================================================")
# print("============================================================")
# print("============================================================")
# print(large_spatial_demos)

# random.shuffle(small_spatial_demos)
# random.shuffle(large_spatial_demos)

# selected_right_small_spatial = small_spatial_demos[:len(small_spatial_demos) // 2]
# selected_left_small_spatial = small_spatial_demos[len(small_spatial_demos) // 2:]

# selected_right_large_spatial = large_spatial_demos[:len(large_spatial_demos) // 2]
# selected_left_large_spatial = large_spatial_demos[len(large_spatial_demos) // 2 : ]

# selected_agentview_dict_small_spatial = {
#     "shoulderview_left_image" : small_spatial_demos
# }

# selected_agentview_dict_large_spatial = {
#     "shoulderview_left_image" : large_spatial_demos
# }

# with open(pickle_path_1, "wb") as f:
#     pickle.dump(selected_agentview_dict_small_spatial, f)

# with open(pickle_path_2, "wb") as f:
#     pickle.dump(selected_agentview_dict_large_spatial, f)



# demo_list = []

# for demo in demos:
#     demo_list.append(demo)

# random.shuffle(demo_list)

# print(len(demo_list) // 2)

# selected_right = demo_list[:len(demo_list) // 2]
# selected_left = demo_list[len(demo_list) // 2 :]

# selected_agent_view_dict = {
#     "shoulderview_right_image" : selected_right,
#     "shoulderview_left_image" : selected_left
# }


# print(selected_agent_view_dict)

demo_file.close()

# with open(pickle_path, "wb") as f:
#     pickle.dump(selected_agent_view_dict, f)


