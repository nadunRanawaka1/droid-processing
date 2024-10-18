import h5py
import time
import os



def create_target_dataset(dataset_path, save_dir, target_num):

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    target_dataset_path = os.path.join(save_dir, f"{target_num}_target_dataset.hdf5")

    print(f"Creating target dataset: {target_dataset_path}")
    start = time.time()

    with h5py.File(dataset_path, 'r') as dataset:
        dataset_grp = dataset['data']
        with h5py.File(target_dataset_path, 'w') as target_dataset:
            
            target_grp = target_dataset.create_group('data')
            target_grp.attrs['env_args'] = dataset_grp.attrs['env_args']
            
            num_written = 0
            # Copy over demos
            for demo in dataset_grp:
                if (num_written % 10) == 0:
                    print(f"Processed demo: {num_written}. Time elapsed: {time.time() - start}")
                target_grp.copy(dataset_grp[demo], f'demo_{num_written}')
                num_written += 1

                if num_written >= target_num:
                    break

target_nums = [5]

dataset_path = "/nethome/nkra3/robomimic-v2/datasets/collector/baking/obj_spat_datasets/large_spat.hdf5"
save_dir = f"/nethome/nkra3/robomimic-v2/datasets/retriever/baking/target_datasets"

for num in target_nums:
    # target_path = f"/nethome/nkra3/robomimic-v2/datasets/retriever/pour_bowl/target_datasets/"
    create_target_dataset(dataset_path, save_dir, num)