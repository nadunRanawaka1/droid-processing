import h5py
import random

blue_bowl_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_bowl_in_box/put_bowl_in_box_blue_bowl_demo.hdf5"
green_bowl_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_bowl_in_box/put_bowl_in_box_green_bowl_demo.hdf5"

blue_bowl_file = h5py.File(blue_bowl_fn, "r")
green_bowl_file = h5py.File(green_bowl_fn, "r")

blue_bowl_grp = blue_bowl_file['data']
green_bowl_grp = green_bowl_file['data']

green_demo_list = []

for demo in green_bowl_grp:
    green_demo_list.append(demo)
random.shuffle(green_demo_list)

blue_demo_list = []
for demo in blue_bowl_grp:
    blue_demo_list.append(demo)
random.shuffle(blue_demo_list)


### Create target dataset
target_dataset_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_bowl_in_box/obj_tex_datasets/target_dataset.hdf5"

with h5py.File(target_dataset_fn, "w") as target_dataset:
    target_dataset_grp = target_dataset.create_group('data')
    target_dataset_grp.attrs['env_args'] = blue_bowl_grp.attrs['env_args']

    total = 0
    # Start copying over demos
    for i in range(10):
        target_dataset_grp.copy(blue_bowl_grp[f"demo_{i}"], f"demo_{i}")
        
        total += blue_bowl_grp[f"demo_{i}"].attrs['num_samples']
    
    target_dataset_grp.attrs['total'] = total


### Create SmallBaseConfig i.e. green bowl only dataset

# small_base_config_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_bowl_in_box/obj_tex_datasets/green_bowl_only.hdf5"

# with h5py.File(small_base_config_fn, 'w') as dataset:
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = green_bowl_grp.attrs['env_args']

#     total = 0
#     for i in range(50):
#         green_demo = green_demo_list[i]
#         dataset_grp.copy(green_bowl_grp[green_demo], f"demo_{i}")
#         total += green_bowl_grp[green_demo].attrs['num_samples']
#     dataset_grp.attrs['total'] = total


# ### Create green + blue

# green_and_blue_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_bowl_in_box/obj_tex_datasets/green_and_blue.hdf5"

# with h5py.File(green_and_blue_fn, 'w') as dataset:
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = green_bowl_grp.attrs['env_args']

#     total  = 0
#     num_written = 0
#     for i in range(25):
#         green_demo = green_demo_list[i]
#         blue_demo = blue_demo_list[i]

#         dataset_grp.copy(green_bowl_grp[green_demo], f"demo_{num_written}")
#         num_written += 1
#         total += green_bowl_grp[green_demo].attrs['num_samples']

#         dataset_grp.copy(blue_bowl_grp[blue_demo], f"demo_{num_written}")
#         num_written += 1
#         total += blue_bowl_grp[blue_demo].attrs['num_samples']
#     dataset_grp.attrs['total'] = total