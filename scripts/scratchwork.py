import pickle
import nexusformat.nexus as nx
import h5py
import random


demo_fn = "/media/nadun/Data/Droid/droid_hdf5/modified_datasets/droid_100_selected_agentview.hdf5"

pickle_path = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/selected_agent_view_dict_droid_100.pkl"

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)
#
# demo_file = h5py.File(demo_fn)
#
# demos = demo_file['data']
#
# demo_list = []
#
# for demo in demos:
#     demo_list.append(demo)
#
# random.shuffle(demo_list)
#
# print(len(demo_list) // 2)
#
# selected_right = demo_list[:len(demo_list) // 2]
# selected_left = demo_list[len(demo_list) // 2 :]
#
# selected_agent_view_dict = {
#     "shoulderview_right_image" : selected_right,
#     "shoulderview_left_image" : selected_left
# }


print(selected_agent_view_dict)

demo_file.close()

with open(pickle_path, "wb") as f:
    pickle.dump(selected_agent_view_dict, f)


