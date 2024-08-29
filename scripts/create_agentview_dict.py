import pickle
import h5py
import nexusformat.nexus as nx
import random
from copy import deepcopy
import os

demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/cam_pose_demo.hdf5"

# demo_file = nx.nxload(demo_fn)
# print(demo_file.tree)

demo_file = h5py.File(demo_fn, 'r')
data = demo_file['data']

demo_list = []
for demo in data:
    demo_list.append(demo)


N = len(demo_list)
# SELECTING RIGHT Image AS AGENTVIEW
right_image_dict = {"right_image": deepcopy(demo_list)} # DONE

# SELECTING LEFT SHOULDERVIEW AS AGENTVIEW (SMALL_BASE_CONFIG)
shoulderview_left_image_dict = {"shoulderview_left_image": deepcopy(demo_list)}

# SELECTING LEFT IMAGE + SHOULDERVIEW LEFT AS AGENTVIEW
shoulderview_left_image_agentview = random.sample(demo_list, N//2)
left_image_agentview = [d for d in demo_list if d not in shoulderview_left_image_agentview]

left_image_shoulderview_left_dict = {"shoulderview_left_image": deepcopy(shoulderview_left_image_agentview),
                                    "left_image": deepcopy(left_image_agentview)
                                    }

# SELECTING RIGHT + LEFT AS AGENTVIEW
right_image_agentview = random.sample(demo_list, N//2)
left_image_agentview = [d for d in demo_list if d not in right_image_agentview]


left_right_image_dict = {"right_image": deepcopy(right_image_agentview),
                        "left_image": deepcopy(left_image_agentview)} 

# SELECTING RIGHT VIEW + SHOULDERVIEW LEFT AS AGENTVIEW
right_image_agentview = random.sample(demo_list, N//2)
shoulderview_left_image_agentview = [d for d in demo_list if d not in right_image_agentview]

right_image_shoulderview_left_image_dict = {"right_image": deepcopy(right_image_agentview), 
                                        "shoulderview_left_image": deepcopy(shoulderview_left_image_agentview)}

# SELECTING LEFT AND RIGHT VIEW + ALL SHOULDERVIEWS
shuffled = deepcopy(demo_list)
random.shuffle(shuffled)

split1 = N // 4
split2 = 2 * N // 4
split3 = 3 * N // 4

right_image_agentview = sorted(shuffled[:split1])
left_image_agentview = sorted(shuffled[split1:split2])

shoulderview_right_image_agentview = sorted(shuffled[split2:split3])
shoulderview_left_image_agentview = sorted(shuffled[split3:])

all_views_agentview_dict = {"right_image": deepcopy(right_image_agentview),
                            "left_image": deepcopy(left_image_agentview),
                            "shoulderview_right_image": deepcopy(shoulderview_right_image_agentview),
                            "shoulderview_left_image": deepcopy(shoulderview_left_image_agentview)
} # DONE


# GOOD DATASET, SELECTING RIGHTVIEW AND SHOULDERVIEW RIGHT AS AGENTVIEW

right_image_agentview = random.sample(demo_list, N//2)
shoulderview_right_image_agentview = [d for d in demo_list if d not in right_image_agentview]

right_shoulderview_right_dict = {"right_image": deepcopy(right_image_agentview),
                                "shoulderview_right_image": deepcopy(shoulderview_right_image_agentview)
                                } 

# BEST DATASET, SELECTING SHOUDLERVIEW RIGHT AS AGENTVIEW

shoulderview_right_dict =  {"shoulderview_right_image": deepcopy(demo_list)}

# Target DATASET, SELECT 10 DEMOS AND SET AGENTVIEW
# shoulderview_right_image_agentview = random.sample(demo_list, 10)

# target_dataset_dict = {"shoulderview_right_image": deepcopy(demo_list)} 

# print(target_dataset_dict)

# ===================================================================================================================== #


save_folder = '/nethome/nkra3/flash7/Droid/droid-processing/agentview_dicts/screwdriver'

# with open(os.path.join(save_folder, "shoulderview_left_image_agentview_dict.pkl"), 'wb') as f:
#     pickle.dump(shoulderview_left_image_dict, f)

# with open(os.path.join(save_folder, "left_right_image_agentview_dict.pkl"), 'wb') as f:
#     pickle.dump(left_right_image_dict, f)

# with open(os.path.join(save_folder, "right_image_shoulderview_left_image_dict.pkl"), 'wb') as f:
#     pickle.dump(right_image_shoulderview_left_image_dict, f)

# with open(os.path.join(save_folder, "all_views_agentview_dict.pkl"), 'wb') as f:
#     pickle.dump(all_views_agentview_dict, f)

# with open(os.path.join(save_folder, "right_shoulderview_right_dict.pkl"), 'wb') as f:
#     pickle.dump(right_shoulderview_right_dict, f)

# with open(os.path.join(save_folder, "target_dataset_dict.pkl"), 'wb') as f:
#     pickle.dump(target_dataset_dict, f)

# with open(os.path.join(save_folder, "left_image_shoulderview_left_dict.pkl"), 'wb') as f:
#     pickle.dump(left_image_shoulderview_left_dict, f)

with open(os.path.join(save_folder, "shoulderview_right_dict.pkl"), 'wb') as f:
    pickle.dump(shoulderview_right_dict, f)