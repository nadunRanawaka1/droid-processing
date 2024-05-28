import h5py
import argparse
import pickle
import time


### This script will select which real world camera to set as "agentview" for a given dataset

def select_agent_view_in_dict(agentview_dict_fn, dataset_path, processed_dataset_path):
    """

    :param agentview_dict_fn: pickle file of dict
    :param dataset_path: original dataset path
    :param processed_dataset_path: where to save the processed dataset
    """
    f = open(agentview_dict_fn, 'rb')
    agentview_dict = pickle.load(f) # agentview dict : {"real_camera_name" : list of demos to set this camera as agentview}

    start = time.time()

    with h5py.File(dataset_path, "r") as src_dataset:

        num_written = 0
        src_dataset_grp = src_dataset['data']

        
        with h5py.File(processed_dataset_path, "w") as processed_dataset:

            processed_dataset_grp = processed_dataset.create_group("data")

            for camera in agentview_dict:
                selected_demos = agentview_dict[camera]

                for demo in selected_demos:

                    if (num_written % 20) == 0:
                        print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")


                    #First, copy all data from the source to the new processed dataset
                    processed_dataset_grp.copy(src_dataset_grp[demo], f"demo_{num_written}")

                    # Next, set the selected agentview camera
                    processed_dataset_grp[f"demo_{num_written}/obs/selected_agentview_image"] = processed_dataset_grp[f"demo_{num_written}/obs/{camera}"]
                    processed_dataset_grp[f"demo_{num_written}"].attrs["Original_Droid_Demo_Number"] = demo

                    num_written += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agentview_dict_path",
                        type=str,
                        required=True)
    parser.add_argument("--dataset_path",
                        type=str,
                        required=True)
    parser.add_argument("--processed_dataset_path",
                        type=str,
                        required=True)

    args = parser.parse_args()
    select_agent_view_in_dict(args.agentview_dict_path, args.dataset_path, args.processed_dataset_path)




