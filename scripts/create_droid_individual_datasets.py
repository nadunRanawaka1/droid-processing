import h5py
import pickle
import time
import os


droid_path = "/nethome/nkra3/flash7/Droid/droid_hdf5/droid.hdf5"
processed_dataset_folder = "/nethome/nkra3/flash7/Droid/droid_hdf5/exp_datasets/single_task_datasets"



fp = "/nethome/nkra3/flash7/Droid/droid-processing/droid_filter_keys/lang_1_to_demos.pkl"

f = open(fp, "rb")

lang_1_to_demos = pickle.load(f)

start = time.time()

with h5py.File(droid_path, "r") as src_dataset:

    src_dataset_grp = src_dataset['data']

    # Create individual datasets for each unique task
    for lang in lang_1_to_demos:

        print(f"Now creating dataset: {lang}")

        num_written = 0
        demos = lang_1_to_demos[lang]

        task_name = lang.replace(" ", "_")
        processed_dataset_name = f"{task_name}_demos.hdf5"
        processed_dataset_path = os.path.join(processed_dataset_folder, processed_dataset_name)

        with h5py.File(processed_dataset_path, "w") as processed_dataset:        

            processed_dataset_grp = processed_dataset.create_group("data")

            for demo in demos:

                if (num_written % 20) == 0:
                    print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")

                #First, copy all data from the source to the new processed dataset
                processed_dataset_grp.copy(src_dataset_grp[demo], f"demo_{num_written}")

                processed_dataset_grp[f"demo_{num_written}"].attrs["Original_Droid_Demo_Number"] = demo

                num_written += 1


