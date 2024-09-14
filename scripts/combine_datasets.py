import h5py
import nexusformat.nexus as nx

first_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/green_can_100_demos_demo.hdf5"
second_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/left_cam_high_75_demos_demo.hdf5"
combined_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/green_can_100_demos_new_campose.hdf5"

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
        if num_written == 50:
            break


    for demo in second_grp:
        print(f"Proccessing demo: {demo}")
        grp.copy(second_grp[demo], f"demo_{num_written}")
        num_written += 1

        total += second_grp[demo].attrs['num_samples']
        if num_written == 100:
            break


first_file.close()
second_file.close()