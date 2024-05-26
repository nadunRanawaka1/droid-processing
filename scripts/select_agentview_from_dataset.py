import h5py
import argparse
import pickle


### This script will select which real world camera to set as "agentview" for a given dataset

agentview_dict_fn = "" # pickle file
f = open(agentview_dict_fn, 'rb')
agentview_dict = pickle.load(f) # agentview dict : {"real_camera_name" : list of demos to set this camera as agentview}

dataset_path = "" #hdf5 filepath
processed_dataset_path = ""
with h5py.File(dataset_path, "r") as src_dataset:

    num_written = 0
    src_dataset_grp = src_dataset['data']

    with h5py.File(processed_dataset_path, "w") as processed_dataset:

        processed_dataset_grp = processed_dataset.create_group("data")

        for camera in agentview_dict:
            selected_demos = agentview_dict[camera]

            for demo in selected_demos:

                #First, copy all data from the source to the new processed dataset
                processed_dataset_grp.copy(processed_dataset_grp[demo], f"demo_{num_written}")
                
                # Next, set the selected agentview camera
                processed_dataset_grp[f"demo_{num_written}/obs/selected_agentview_image"] = processed_dataset_grp[f"demo_{num_written}/obs/{camera}"]

                num_written += 1
                





