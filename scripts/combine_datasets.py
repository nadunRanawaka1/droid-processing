import h5py
import nexusformat.nexus as nx

first_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/cam_pose_datasets/target_dataset.hdf5"
second_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/30_fully_extended_red_small_demo.hdf5"
combined_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/cam_pose_datasets/new_target_dataset.hdf5"

first_file = h5py.File(first_fn, 'r')
second_file = h5py.File(second_fn, 'r')


first_grp = first_file['data']
second_grp = second_file['data']


with h5py.File(combined_fn, 'w') as combined_file:
    grp = combined_file.create_group('data')
    grp.attrs['env_args'] = first_grp.attrs['env_args']

    num_written = 0
    total = 0
    for demo in first_grp:
        print(f"Proccessing demo: {demo}")
        grp.copy(first_grp[demo], f"demo_{num_written}")
        num_written += 1

        total += first_grp[demo].attrs['num_samples']


    for demo in second_grp:
        print(f"Proccessing demo: {demo}")
        grp.copy(second_grp[demo], f"demo_{num_written}")
        grp[f"demo_{num_written}/obs/selected_agentview_image"] = grp[f"demo_{num_written}/obs/shoulderview_right_image"]
        num_written += 1

        total += second_grp[demo].attrs['num_samples']


first_file.close()
second_file.close()