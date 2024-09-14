import h5py
import argparse
import pickle
import time
import random
import os
from copy import deepcopy


### This script will select which real world camera to set as "agentview" for a given dataset

def select_agent_view_in_dict(agentview_dict, dataset_path, processed_dataset_path):
    """

    :param agentview_dict_fn: pickle file of dict
    :param dataset_path: original dataset path
    :param processed_dataset_path: where to save the processed dataset
    """
    # f = open(agentview_dict_fn, 'rb')
    # agentview_dict = pickle.load(f) # agentview dict : {"real_camera_name" : list of demos to set this camera as agentview}
    

    start = time.time()

    with h5py.File(dataset_path, "r") as src_dataset:

        num_written = 0
        src_dataset_grp = src_dataset['data']

        
        with h5py.File(processed_dataset_path, "w") as processed_dataset:

            processed_dataset_grp = processed_dataset.create_group("data")

            print(f"CREATING DATASET: {processed_dataset_path}")

            #copy over env args
            processed_dataset_grp.attrs['env_args'] = src_dataset_grp.attrs['env_args']
            total = 0

            for camera in agentview_dict:
                selected_demos = agentview_dict[camera]
                
                for demo in selected_demos:

                    if (num_written % 10) == 0:
                        print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")


                    #First, copy all data from the source to the new processed dataset
                    processed_dataset_grp.copy(src_dataset_grp[demo], f"demo_{num_written}")

                    # Next, set the selected agentview camera

                    if "selected_agentview_image" in processed_dataset_grp[f"demo_{num_written}/obs"]:
                        del processed_dataset_grp[f"demo_{num_written}/obs/selected_agentview_image"]
                    processed_dataset_grp[f"demo_{num_written}/obs/selected_agentview_image"] = processed_dataset_grp[f"demo_{num_written}/obs/{camera}"]
                    # processed_dataset_grp[f"demo_{num_written}"].attrs["Original_Droid_Demo_Number"] = demo

                    num_written += 1
                    total += src_dataset_grp[demo].attrs['num_samples']
                    
            processed_dataset_grp.attrs['total'] = total



def create_target_datasets(demo_fn, processed_datasets_folder):

    if not os.path.exists(processed_datasets_folder):
        os.makedirs(processed_datasets_folder)

    demo_file = h5py.File(demo_fn, 'r')
    data = demo_file['data']

    demo_list = []
    for demo in data:
        demo_list.append(demo)

    random.shuffle(demo_list)

    dict_list = []


    # # CREATE 10 TARGET DATASET (shoulderview_right AS AGENTVIEW)

    target_dict_10_demos =  {"shoulderview_right_image": deepcopy(demo_list[:10])}
    target_dict_path_10_demos = os.path.join(processed_datasets_folder, "10_target_dataset.hdf5")

    dict_list.append((target_dict_10_demos, target_dict_path_10_demos))

    # # CREATE 20 TARGET DATASET (LEFT AS AGENTVIEW)

    target_dict_20_demos =  {"shoulderview_right_image": deepcopy(demo_list[:20])}
    target_dict_path_20_demos = os.path.join(processed_datasets_folder, "20_target_dataset.hdf5")

    dict_list.append((target_dict_20_demos, target_dict_path_20_demos))

     # # CREATE 30 TARGET DATASET ( LEFT AS AGENTVIEW)

    target_dict_30_demos =  {"shoulderview_right_image": deepcopy(demo_list[:30])}
    target_dict_path_30_demos = os.path.join(processed_datasets_folder, "30_target_dataset.hdf5")

    dict_list.append((target_dict_30_demos, target_dict_path_30_demos))

    return dict_list



def create_agentview_dicts(demo_fn, processed_datasets_folder):
    # demo_file = nx.nxload(demo_fn)
    # print(demo_file.tree)
    if not os.path.exists(processed_datasets_folder):
        os.makedirs(processed_datasets_folder)

    demo_file = h5py.File(demo_fn, 'r')
    data = demo_file['data']

    demo_list = []
    for demo in data:
        demo_list.append(demo)

    random.shuffle(demo_list)

    dict_list = []

    N = len(demo_list)


    # # SELECTING RIGHT Image AS AGENTVIEW
    # right_image_dict = {"right_image": deepcopy(demo_list)} # DONE
    # right_image_dict_path = os.path.join(processed_datasets_folder, "right_image_as_agentview.hdf5")
    # dict_list.append((right_image_dict, right_image_dict_path))

    # # SELECTING LEFT Image as AGENTVIEW
    left_image_dict = {"left_image": deepcopy(demo_list)}
    left_image_dict_path = os.path.join(processed_datasets_folder, "left_image.hdf5")
    dict_list.append((left_image_dict, left_image_dict_path))


    # # SELECTING RIGHT SHOULDERVIEW AS AGENTVIEW (SMALL_BASE_CONFIG)
    shoulderview_right_image_dict = {"shoulderview_right_image": deepcopy(demo_list)}
    shoulderview_right_image_dict_path = os.path.join(processed_datasets_folder, "shoulderview_right_image_SBC.hdf5")
    dict_list.append((shoulderview_right_image_dict, shoulderview_right_image_dict_path))

    # # SELECT SHOULDERVIEW LEFT AS AGENTVIEW
    # shoulderview_left_image_dict = {"shoulderview_left_image": deepcopy(demo_list)}
    # shoulderview_left_image_dict_path = os.path.join(processed_datasets_folder, "shoulderview_left_image.hdf5")
    # dict_list.append((shoulderview_left_image_dict, shoulderview_left_image_dict_path))


    # # SELECTING LEFT AND RIGHT VIEW AS AGENTVIEW
    # right_image_agentview = demo_list[:N//2]
    # left_image_agentview = [d for d in demo_list if d not in right_image_agentview]


    # left_right_image_dict = {"right_image": deepcopy(right_image_agentview),
    #                     "left_image": deepcopy(left_image_agentview)} 
    
    # left_right_image_dict_path = os.path.join(processed_datasets_folder, "left_image_and_right_image.hdf5")
    # dict_list.append((left_right_image_dict, left_right_image_dict_path))

    # # SELECTING RIGHTVIEW AND SHOULDERVIEW RIGHT AS AGENTVIEW
    right_image_agentview = demo_list[:N//2]
    shoulderview_right_image_agentview = [d for d in demo_list if d not in right_image_agentview]

    right_shoulderview_right_dict = {"right_image": deepcopy(right_image_agentview),
                                    "shoulderview_right_image": deepcopy(shoulderview_right_image_agentview)}
    
    right_shoulderview_right_dict_path = os.path.join(processed_datasets_folder, "right_image_and_shoulderview_right_image.hdf5")
    dict_list.append((right_shoulderview_right_dict, right_shoulderview_right_dict_path))

    ### SELECTING ALL VIEWS AS AGENTVIEW

    split1 = N // 4
    split2 = 2 * N // 4
    split3 = 3 * N // 4

    right_image_agentview = sorted(demo_list[:split1])
    left_image_agentview = sorted(demo_list[split1:split2])

    shoulderview_right_image_agentview = sorted(demo_list[split2:split3])
    shoulderview_left_image_agentview = sorted(demo_list[split3:])

    all_views_agentview_dict = {"right_image": deepcopy(right_image_agentview),
                                "left_image": deepcopy(left_image_agentview),
                                "shoulderview_right_image": deepcopy(shoulderview_right_image_agentview),
                                "shoulderview_left_image": deepcopy(shoulderview_left_image_agentview)
                                }

    all_views_agentview_dict_path = os.path.join(processed_datasets_folder, "all_views.hdf5")

    dict_list.append((all_views_agentview_dict, all_views_agentview_dict_path))


    return dict_list
    

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument("--agentview_dict_path",
    #                     type=str,
    #                     required=True)
    # parser.add_argument("--processed_dataset_path",
    #                     type=str,
    #                     required=True)

    parser.add_argument("--dataset_path",
                        type=str,
                        required=True)
    parser.add_argument("--target_path",
                        type=str,
                        required=True)
    
    parser.add_argument("--processed_datasets_folder", 
                        type=str,
                        required=True)

    args = parser.parse_args()

    ### Create the cotraining datasets

    # agentview_dicts_and_save_paths = create_agentview_dicts(args.dataset_path, args.processed_datasets_folder)

    # for (agentview_dict, save_path) in agentview_dicts_and_save_paths:

    #     select_agent_view_in_dict(agentview_dict, args.dataset_path, save_path)

    
    ### Create the target datasets

    target_dicts_and_save_paths = create_target_datasets(args.target_path, args.processed_datasets_folder)

    for (agentview_dict, save_path) in target_dicts_and_save_paths:

        select_agent_view_in_dict(agentview_dict, args.target_path, save_path)




