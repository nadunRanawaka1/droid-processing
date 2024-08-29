import h5py
import random

def get_grp_and_demo_list(demo_fn):
    file = h5py.File(demo_fn, 'r')
    grp = file['data']
    demo_list = []

    for demo in grp:
        demo_list.append(demo)
    random.shuffle(demo_list)
    return grp, demo_list


red_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/cam_pose_demo.hdf5"
pink_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/pink_demo.hdf5"
blue_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/blue_demo.hdf5"
yellow_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/yellow_demo.hdf5"
green_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/original_datasets/green_demo.hdf5"

COTRAINING_DEMOS = 100


red_grp, red_demo_list = get_grp_and_demo_list(red_fn)
pink_grp, pink_demo_list = get_grp_and_demo_list(pink_fn)
blue_grp, blue_demo_list = get_grp_and_demo_list(blue_fn)
yellow_grp, yellow_demo_list = get_grp_and_demo_list(yellow_fn)
green_grp, green_demo_list = get_grp_and_demo_list(green_fn)


### Create target dataset, pink is the target
# target_dataset_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/target_dataset.hdf5"

# with h5py.File(target_dataset_fn, "w") as target_dataset:
#     target_dataset_grp = target_dataset.create_group('data')
#     target_dataset_grp.attrs['env_args'] = pink_grp.attrs['env_args']

#     total = 0
#     # Start copying over demos
#     for i in range(10):
#         target_dataset_grp.copy(pink_grp[f"demo_{i}"], f"demo_{i}")
        
#         total += pink_grp[f"demo_{i}"].attrs['num_samples']
    
#     target_dataset_grp.attrs['total'] = total


### Create SmallBaseConfig i.e. red only dataset

# small_base_config_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red_only_sbc.hdf5"
# print("Creating small base config")

# with h5py.File(small_base_config_fn, 'w') as dataset:
    
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

#     total = 0
#     for i in range(100):
#         print(f"Processing batch: {i}")
#         demo = red_demo_list[i]
#         dataset_grp.copy(red_grp[demo], f"demo_{i}")
#         total += red_grp[demo].attrs['num_samples']
#     dataset_grp.attrs['total'] = total


### Create red + blue

# green_and_blue_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red_and_blue.hdf5"
# print("Creating red and blue dataset")
# with h5py.File(green_and_blue_fn, 'w') as dataset:
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

#     total  = 0
#     num_written = 0
#     for i in range(50):
#         print(f"Processing batch: {i}")
#         red_demo = red_demo_list[i]
#         blue_demo = blue_demo_list[i]

#         dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
#         num_written += 1
#         total += red_grp[red_demo].attrs['num_samples']

#         dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
#         num_written += 1
#         total += blue_grp[blue_demo].attrs['num_samples']
#     dataset_grp.attrs['total'] = total



### Create red + blue + yellow

fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red+blue+yellow.hdf5"
print("Creating red and blue and yellow dataset")

with h5py.File(fn, 'w') as dataset:
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    num_written = 0

    for i in range(len(yellow_demo_list)):
        print(f"Processing batch: {i}")
        if num_written > COTRAINING_DEMOS:
            break

        red_demo = red_demo_list[i]
        blue_demo = blue_demo_list[i]
        yellow_demo = yellow_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
        num_written += 1
        total += yellow_grp[yellow_demo].attrs['num_samples']

    dataset_grp.attrs['total'] = total


### Create red + blue + yellow + green

fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red+blue+yellow+green.hdf5"
print("Creating red and blue and yellow and green dataset")

with h5py.File(fn, 'w') as dataset: 
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    num_written = 0

    for i in range(len(green_demo_list)):
        print(f"Processing batch: {i}")
        if num_written > COTRAINING_DEMOS:
            break

        red_demo = red_demo_list[i]
        blue_demo = blue_demo_list[i]
        yellow_demo = yellow_demo_list[i]
        green_demo = green_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
        num_written += 1
        total += yellow_grp[yellow_demo].attrs['num_samples']

        dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
        num_written += 1
        total += green_grp[green_demo].attrs['num_samples']

    dataset_grp.attrs['total'] = total


### Create all colors

all_colors_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/all_colors_new.hdf5"
print("Creating all colors dataset")
with h5py.File(all_colors_fn, 'w') as dataset:
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    num_written = 0
    for i in range(len(green_demo_list)):
        if num_written > COTRAINING_DEMOS:
            break
        print(f"Processing batch: {i}")

        red_demo = red_demo_list[i]
        blue_demo = blue_demo_list[i]
        pink_demo = pink_demo_list[i]
        yellow_demo = yellow_demo_list[i]
        green_demo = green_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(pink_grp[pink_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
        num_written += 1
        total += yellow_grp[yellow_demo].attrs['num_samples']

        dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
        num_written += 1
        total += green_grp[green_demo].attrs['num_samples']

    dataset_grp.attrs['total'] = total