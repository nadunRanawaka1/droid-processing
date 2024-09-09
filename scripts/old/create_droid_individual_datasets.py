import h5py
import time
import os


droid_path = <PATH TO DROID>
processed_dataset_folder = <WHERE TO PUT THE SINGLE TASK DATASETS>

if not os.path.exists(processed_dataset_folder):
     os.makedirs(processed_dataset_folder)

lang_to_demos = {"lang instruction": <list of demos>}

start = time.time()
tasks = 0

with h5py.File(droid_path, "r") as src_dataset:
    src_dataset_grp = src_dataset['data']

    for lang in lang_to_demos:
        
        demos = lang_to_demos[lang]
        
        print(f"Creating dataset for task : {lang}")
        processed_dataset_name = f"{lang}_demos.hdf5"
        processed_dataset_path = os.path.join(processed_dataset_folder, processed_dataset_name)

        num_written = 0

        with h5py.File(processed_dataset_path, "w") as processed_dataset:
                processed_dataset_grp = processed_dataset.create_group("data")

                for demo in demos:
                    if (num_written % 20) == 0:
                        print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")

                    #Copy all data from the source to the new processed dataset
                    processed_dataset_grp.copy(src_dataset_grp[demo], f"demo_{num_written}")
                    processed_dataset_grp[f"demo_{num_written}"].attrs["Original_Droid_Demo_Number"] = demo

                    num_written += 1



