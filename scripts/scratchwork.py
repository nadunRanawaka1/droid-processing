import pickle
import nexusformat.nexus as nx
import h5py
import random
import re

demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/place_bowl_on_plate/place_bowl_on_plate_new_config_demo.hdf5"

# demo_file = nx.nxload(demo_fn)
# print(demo_file.tree)


# pickle_path_1 = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/selected_agent_view_mix_out_of_spatial_distribution.pkl"
# pickle_path_2 = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/selected_agent_view_mix_in_spatial_distribution.pkl"

demo_file = h5py.File(demo_fn, 'r')


demos = demo_file['data']



# ### FOR SELECTING CAMERAS

# masks = demo_file['mask']

# demos_not_in_spatial = masks['pick_location_not_in_target'][:].tolist()
# demos_in_spatial = masks['pick_location_in_target'][:].tolist()
# #
# for i, demo in enumerate(demos_not_in_spatial):
#     demos_not_in_spatial[i] = str(demo, encoding='utf-8')

# for i, demo in enumerate(demos_in_spatial):
#     demos_in_spatial[i] = str(demo, encoding='utf-8')
# #
# #
# # # print(small_spatial_demos)
# # # print("============================================================")
# # # print("============================================================")
# # # print("============================================================")
# # # print(large_spatial_demos)
# #
# random.shuffle(demos_not_in_spatial)
# random.shuffle(demos_in_spatial)

# selected_right_not_in_spatial = demos_not_in_spatial[:len(demos_not_in_spatial) // 2]
# selected_left_not_in_spatial = demos_not_in_spatial[len(demos_not_in_spatial) // 2:]

# selected_right_in_spatial = demos_in_spatial[:len(demos_in_spatial) // 2]
# selected_left_in_spatial = demos_in_spatial[len(demos_in_spatial) // 2 :]


# #
# # # selected_agentview_dict_small_spatial = {
# # #     "shoulderview_left_image" : small_spatial_demos
# # # }
# #
# # selected_agentview_dict_large_spatial = {
# #     "shoulderview_left_image" : selected_left_large_spatial,
# #     "shoulderview_right_image": selected_right_large_spatial
# # }

# selected_agent_view_dict_not_in_spatial = {
#     "shoulderview_left_image" : selected_left_not_in_spatial,
#     "shoulderview_right_image" : selected_right_not_in_spatial
# }

# selected_agent_view_dict_in_spatial = {
#     "shoulderview_left_image" : selected_left_in_spatial,
#     "shoulderview_right_image" : selected_right_in_spatial
# }

# # print(selected_agent_view_dict_not_in_spatial)

# #
# with open(pickle_path_1, "wb") as f:
#     pickle.dump(selected_agent_view_dict_not_in_spatial, f)

# with open(pickle_path_2, "wb") as f:
#     pickle.dump(selected_agent_view_dict_in_spatial, f)
#
#
#
demo_list = []

for demo in demos:
    demo_list.append(demo)
# #
# random.shuffle(demo_list)
# #
# # # print(len(demo_list) // 2)
# #
# # # selected_right = demo_list[:len(demo_list) // 2]
# # # selected_left = demo_list[len(demo_list) // 2 :]
# #
# # # selected_agent_view_dict = {
# # #     "shoulderview_right_image" : selected_right,
# # #     "shoulderview_left_image" : selected_left
# # # }
# #
# #
# # # print(selected_agent_view_dict)
# #

selected_agent_view_dict = {
    "agentview_image":demo_list
}
demo_file.close()

print(selected_agent_view_dict)
#
with open("/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/agentview_as_agentview_new_target_dataset.pkl", "wb") as f:
    pickle.dump(selected_agent_view_dict, f)




### RANDOM SCRATCHWORK
