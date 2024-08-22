import h5py
import random

small_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/cam_pose_demo.hdf5"
med_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/med_spatial_demo.hdf5"
large_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/large_spatial_demo.hdf5"

small_file = h5py.File(small_fn, 'r')
med_file = h5py.File(med_fn, 'r')
large_file = h5py.File(large_fn, 'r')

small_grp = small_file['data']
med_grp = med_file['data']
large_grp = large_file['data']

small_demo_list = []
for demo in small_grp:
    small_demo_list.append(demo)

med_demo_list = []
for demo in med_grp:
    med_demo_list.append(demo)

large_demo_list = []
for demo in large_grp:
    large_demo_list.append(demo)

random.shuffle(small_demo_list)
random.shuffle(med_demo_list)
random.shuffle(large_demo_list)

### Create the actual medium demo file (that has 75 demos from the small and 25 from the med spatial)

med_spatial_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/spatial_datasets/med_spat.hdf5"

with h5py.File(med_spatial_fn, 'w') as med_spatial_dataset:
    dataset_grp = med_spatial_dataset.create_group('data')
    dataset_grp.attrs['env_args'] = small_grp.attrs['env_args']

    total = 0
    num_written = 0

    print("Copying over med spatial")
    # First copy over all the med spatial demos
    for demo in med_demo_list:
        print(f"Processing demo: {demo}")
        dataset_grp.copy(med_grp[demo], f"demo_{num_written}")

        num_written += 1
        total += med_grp[demo].attrs['num_samples']

    print("Copying over small spatial")
    # Then copy the small spatial demos
    for i in range(100 - num_written):
        print(f"Processing demo : {i}")
        demo = small_demo_list[i]
        dataset_grp.copy(small_grp[demo], f"demo_{num_written}")
        num_written += 1
        total += small_grp[demo].attrs['num_samples']

    dataset_grp.attrs['total'] = total


### Create the actual large demo file (50 from small, 25 from med and 25 from large)

large_spatial_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/spatial_datasets/large_spat.hdf5"

with h5py.File(large_spatial_fn, 'w') as large_spatial_dataset:
    dataset_grp = large_spatial_dataset.create_group('data')

    dataset_grp.attrs['env_args'] = small_grp.attrs['env_args']

    total = 0
    num_written = 0


    print("Copying over large spatial demos")
    # First copy over all the large spatial demos
    for demo in large_demo_list:
        print(f"Processing demo: {demo}")
        dataset_grp.copy(large_grp[demo], f"demo_{num_written}")

        num_written += 1
        total += large_grp[demo].attrs['num_samples']


    print("Copying over med sptial demos")
    # Then copy over all the med spatial demos
    for demo in med_demo_list:
        print(f"Processing demo: {demo}")
        dataset_grp.copy(med_grp[demo], f"demo_{num_written}")

        num_written += 1
        total += med_grp[demo].attrs['num_samples']


    # Then copy the small spatial demos
    for i in range(100 - num_written):
        demo = small_demo_list[i]
        dataset_grp.copy(small_grp[demo], f"demo_{num_written}")
        num_written += 1
        total += small_grp[demo].attrs['num_samples']

    dataset_grp.attrs['total'] = total


# Next create the target dataset using 10 large spatial demos

target_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/spatial_datasets/target.hdf5"

with h5py.File(target_fn, 'w') as target_dataset:
    dataset_grp = target_dataset.create_group('data')

    dataset_grp.attrs['env_args'] = small_grp.attrs['env_args']

    total = 0
    num_written = 0

    for i in range(10):
        print(f"Copying demo {i} of target")
        demo = large_demo_list[i]
        dataset_grp.copy(large_grp[demo], f"demo_{num_written}")

        num_written += 1
        total += large_grp[demo].attrs['num_samples']
        
    dataset_grp.attrs['total'] = total
