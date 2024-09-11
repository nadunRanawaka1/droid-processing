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




green_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/green_can_100_demos_demo.hdf5"
red_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/red_can_50_demos_demo.hdf5"
purple_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/purple_can_40_demos_demo.hdf5"
orange_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/orange_can_30_demos_demo.hdf5"

COTRAINING_DEMOS = 100


green_grp, green_demo_list = get_grp_and_demo_list(green_fn)
red_grp, red_demo_list = get_grp_and_demo_list(red_fn)
purple_grp, purple_demo_list = get_grp_and_demo_list(purple_fn)
orange_grp, orange_demo_list = get_grp_and_demo_list(orange_fn)



### Create 10 target dataset, orange is the target
target_dataset_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/10_target.hdf5"
with h5py.File(target_dataset_fn, "w") as target_dataset:
    target_dataset_grp = target_dataset.create_group('data')
    target_dataset_grp.attrs['env_args'] = orange_grp.attrs['env_args']

    total = 0
    # Start copying over demos
    for i in range(10):
        target_dataset_grp.copy(orange_grp[f"demo_{i}"], f"demo_{i}")
        
        total += orange_grp[f"demo_{i}"].attrs['num_samples']
    
    target_dataset_grp.attrs['total'] = total


### Create 20 target dataset, orange is the target
target_dataset_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/20_target.hdf5"
with h5py.File(target_dataset_fn, "w") as target_dataset:
    target_dataset_grp = target_dataset.create_group('data')
    target_dataset_grp.attrs['env_args'] = orange_grp.attrs['env_args']

    total = 0
    # Start copying over demos
    for i in range(20):
        target_dataset_grp.copy(orange_grp[f"demo_{i}"], f"demo_{i}")
        
        total += orange_grp[f"demo_{i}"].attrs['num_samples']
    
    target_dataset_grp.attrs['total'] = total

### Create 30 target dataset, orange is the target
target_dataset_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/30_target.hdf5"
with h5py.File(target_dataset_fn, "w") as target_dataset:
    target_dataset_grp = target_dataset.create_group('data')
    target_dataset_grp.attrs['env_args'] = orange_grp.attrs['env_args']

    total = 0
    # Start copying over demos
    for i in range(30):
        target_dataset_grp.copy(orange_grp[f"demo_{i}"], f"demo_{i}")
        
        total += orange_grp[f"demo_{i}"].attrs['num_samples']
    
    target_dataset_grp.attrs['total'] = total



### Create SmallBaseConfig i.e. green only dataset

small_base_config_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/green_SBC.hdf5"
print("Creating small base config")

with h5py.File(small_base_config_fn, 'w') as dataset:
    
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = green_grp.attrs['env_args']

    total = 0
    for i in range(100):
        print(f"Processing demo: {i}")
        demo = green_demo_list[i]
        dataset_grp.copy(green_grp[demo], f"demo_{i}")
        total += green_grp[demo].attrs['num_samples']
    dataset_grp.attrs['total'] = total


### Create green + red

green_and_red_fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/green+red.hdf5"
print("Creating red and green dataset")
with h5py.File(green_and_red_fn, 'w') as dataset:
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total  = 0
    num_written = 0
    for i in range(50):
        print(f"Processing batch: {i}")
        red_demo = red_demo_list[i]
        green_demo = green_demo_list[i]

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
        num_written += 1
        total += green_grp[green_demo].attrs['num_samples']
    dataset_grp.attrs['total'] = total



### Create green + red + purple

fn = "/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/obj_tex_datasets/green+red+purple.hdf5"

print("Creating green and red and purple dataset")

with h5py.File(fn, 'w') as dataset: 
    dataset_grp = dataset.create_group('data')
    dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

    total = 0
    num_written = 0

    for i in range(len(purple_demo_list)):
        print(f"Processing batch: {i}")
        if num_written > COTRAINING_DEMOS:
            break

        
        green_demo = green_demo_list[i]
        red_demo = red_demo_list[i]
        purple_demo = purple_demo_list[i]
        


        dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
        num_written += 1
        total += green_grp[green_demo].attrs['num_samples']

        dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
        num_written += 1
        total += red_grp[red_demo].attrs['num_samples']

        dataset_grp.copy(purple_grp[purple_demo], f"demo_{num_written}")
        num_written += 1
        total += purple_grp[purple_demo].attrs['num_samples']


    for j in range(len(purple_demo_list), 100):

        print(f"Processing batch: {j}")
        if num_written > COTRAINING_DEMOS:
            break

        raise Exception("NEVER SHOULD REACH HERE")

        blue_demo = blue_demo_list[j]
        yellow_demo = yellow_demo_list[j]

        dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
        num_written += 1
        total += blue_grp[blue_demo].attrs['num_samples']

        dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
        num_written += 1
        total += yellow_grp[yellow_demo].attrs['num_samples']


    dataset_grp.attrs['total'] = total





### Create red + blue + yellow + green

# fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red+blue+yellow+green.hdf5"
# print("Creating red and blue and yellow and green dataset")

# with h5py.File(fn, 'w') as dataset: 
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

#     total = 0
#     num_written = 0

#     for i in range(len(green_demo_list)):
#         print(f"Processing batch: {i}")
#         if num_written > COTRAINING_DEMOS:
#             break

#         red_demo = red_demo_list[i]
#         blue_demo = blue_demo_list[i]
#         yellow_demo = yellow_demo_list[i]
#         green_demo = green_demo_list[i]

#         dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
#         num_written += 1
#         total += red_grp[red_demo].attrs['num_samples']

#         dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
#         num_written += 1
#         total += blue_grp[blue_demo].attrs['num_samples']

#         dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
#         num_written += 1
#         total += yellow_grp[yellow_demo].attrs['num_samples']

#         dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
#         num_written += 1
#         total += green_grp[green_demo].attrs['num_samples']

#     dataset_grp.attrs['total'] = total


### Create all colors

# all_colors_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/all_colors_new.hdf5"
# print("Creating all colors dataset")
# with h5py.File(all_colors_fn, 'w') as dataset:
#     dataset_grp = dataset.create_group('data')
#     dataset_grp.attrs['env_args'] = red_grp.attrs['env_args']

#     total = 0
#     num_written = 0
#     for i in range(len(green_demo_list)):
#         if num_written > COTRAINING_DEMOS:
#             break
#         print(f"Processing batch: {i}")

#         red_demo = red_demo_list[i]
#         blue_demo = blue_demo_list[i]
#         pink_demo = pink_demo_list[i]
#         yellow_demo = yellow_demo_list[i]
#         green_demo = green_demo_list[i]

#         dataset_grp.copy(red_grp[red_demo], f"demo_{num_written}")
#         num_written += 1
#         total += red_grp[red_demo].attrs['num_samples']

#         dataset_grp.copy(blue_grp[blue_demo], f"demo_{num_written}")
#         num_written += 1
#         total += blue_grp[blue_demo].attrs['num_samples']

#         dataset_grp.copy(pink_grp[pink_demo], f"demo_{num_written}")
#         num_written += 1
#         total += blue_grp[blue_demo].attrs['num_samples']

#         dataset_grp.copy(yellow_grp[yellow_demo], f"demo_{num_written}")
#         num_written += 1
#         total += yellow_grp[yellow_demo].attrs['num_samples']

#         dataset_grp.copy(green_grp[green_demo], f"demo_{num_written}")
#         num_written += 1
#         total += green_grp[green_demo].attrs['num_samples']

#     dataset_grp.attrs['total'] = total





