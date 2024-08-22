import h5py
import random


red_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/cam_pose_demo.hdf5"
pink_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/pink_demo.hdf5"
blue_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/blue_demo.hdf5"

red_file = h5py.File(red_fn, 'r')
blue_file = h5py.File(blue_fn, "r")
pink_file = h5py.File(pink_fn, "r")

red_grp = red_file['data']
blue_grp = blue_file['data']
pink_grp = pink_file['data']

red_demo_list = []
blue_demo_list = []
pink_demo_list = []

for demo in red_grp:
    red_demo_list.append(demo)
random.shuffle(red_demo_list)

blue_demo_list = []
for demo in blue_grp:
    blue_demo_list.append(demo)
random.shuffle(blue_demo_list)

for demo in pink_grp:
    pink_demo_list.append(demo)
random.shuffle(pink_demo_list)


### Create target dataset, pink is the target
target_dataset_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/target_dataset.hdf5"

with h5py.File(target_dataset_fn, "w") as target_dataset:
    target_dataset_grp = target_dataset.create_group('data')
    target_dataset_grp.attrs['env_args'] = pink_grp.attrs['env_args']

    total = 0
    # Start copying over demos
    for i in range(10):
        target_dataset_grp.copy(pink_grp[f"demo_{i}"], f"demo_{i}")
        
        total += pink_grp[f"demo_{i}"].attrs['num_samples']
    
    target_dataset_grp.attrs['total'] = total


### Create SmallBaseConfig i.e. red only dataset

small_base_config_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red_only_sbc.hdf5"
print("Creating small base config")

with h5py.File(small_base_config_fn, 'w') as dataset:
    
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    for i in range(100):
        print(f"Processing batch: {i}")
        demo = red_demo_list[i]
        dataset_grp.copy(red_grp[demo], f"demo_{i}")
        total += red_grp[demo].attrs['num_samples']
    dataset_grp.attrs['total'] = total


### Create red + blue

green_and_blue_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red_and_blue.hdf5"
print("Creating red and blue dataset")
with h5py.File(green_and_blue_fn, 'w') as dataset:
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total  = 0
    num_written = 0
    for i in range(50):
        print(f"Processing batch: {i}")
        red_demo = red_demo_list[i]
        blue_demo = blue_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']
    dataset_grp.attrs['total'] = total

### Create all colors

all_colors_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/all_colors.hdf5"
print("Creating all colors dataset")
with h5py.File(all_colors_fn, 'w') as dataset:
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    num_written = 0
    for i in range(34):
        print(f"Processing batch: {i}")

        red_demo = red_demo_list[i]
        blue_demo = blue_demo_list[i]
        pink_demo = pink_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(pink_grp[pink_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']
    dataset_grp.attrs['total'] = total