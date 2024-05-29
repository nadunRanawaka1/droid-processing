import pandas as pd
import numpy as np
import pickle


# Setting some stuff for our query

min_target_pick_locations  = [0.361225, -0.296707, 0.124462]
max_target_pick_locations  = [0.759941, -0.197563, 0.262764]

min_target_place_locations = [0.344156, 0.129339, 0.153875]
max_target_place_locations = [0.726725, 0.204588, 0.237842]



# metadata_path = "/media/nadun/Data/Droid/droid_hdf5/droid_metadata.xlsx"
metadata_path = "/home/nadun/Data/Droid/droid_hdf5/droid_metadata.pkl"

df = pd.read_pickle(metadata_path)


# First we filter demos that have pick in the language instruction
pick_mask = df['language_instruction_1'].str.contains('pick', case=False) | df['language_instruction_2'].str.contains('pick', case=False) | df['language_instruction_3'].str.contains('pick', case=False)
pick_df = df[pick_mask]

# Next we filter demos that have place or put

search_strings = ["place", "put"]
place_mask = df['language_instruction_1'].str.contains('|'.join(search_strings), case=False) | df['language_instruction_2'].str.contains('|'.join(search_strings), case=False) | df['language_instruction_3'].str.contains('|'.join(search_strings), case=False)

# Next we pick demos that have only one pick and place action
only_single_picks = pick_df[pick_df['num_gripper_closes'] == 1]
pick_locations = only_single_picks['pick_locations'].tolist()

pick_locations_array = np.concatenate(pick_locations)[:, 0:3]

# Next we filter the demos based on the z location because we want demos that have a z location close to the base of the robot
z_locations = pick_locations_array[:, 2]
z_mask = np.logical_and(z_locations >= -0.05, z_locations <= 0.30)
only_single_picks = only_single_picks[z_mask]

pick_locations = only_single_picks['pick_locations'].tolist()

# Next filter demos that are in our target spatial range
pick_locations_array = np.concatenate(pick_locations)[:, 0:3]

print(only_single_picks.shape)
print(pick_locations_array.shape)


# The small spatial range is within 0.75 std dev of the mean
# small_spatial_range_low = mean_pick_locations - 0.75 * std_pick_locations
# small_spatial_range_high = mean_pick_locations + 0.75 * std_pick_locations

# # The large spatial range is within 3 std dev of the mean
# large_spatial_range_low = mean_pick_locations - std_pick_locations * 3
# large_spatial_range_high = mean_pick_locations + std_pick_locations * 3

# # Now mask out demos where the pick location is within 1 std dev of the mean, this is the small spatial dataset
# small_spatial_range_mask = np.alltrue(np.logical_and(pick_locations_array >= small_spatial_range_low, pick_locations_array <= small_spatial_range_high), axis=1)
# small_spatial_range_df = only_single_picks[small_spatial_range_mask]

# # Mask out demos where the pick location is within 3 std dev of the mean, this is the large spatial dataset
# large_spatial_range_mask = np.alltrue(np.logical_and(pick_locations_array >= large_spatial_range_low, pick_locations_array <= large_spatial_range_high), axis=1)
# large_spatial_range_df = only_single_picks[large_spatial_range_mask]

# small_spatial_range_demos = small_spatial_range_df['Demo']
# print(len(small_spatial_range_demos))
# large_spatial_range_demos = large_spatial_range_df['Demo']

# sampled_small_spatial_range_demos = small_spatial_range_demos.sample(n=1000).to_list()
# sampled_large_spatial_range_demos = large_spatial_range_demos.sample(n=1000).to_list()

# list_string = map(str, sampled_small_spatial_range_demos)
# sampled_small_spatial_range_demos = list(list_string)

# list_string = map(str, sampled_large_spatial_range_demos)
# sampled_large_spatial_range_demos = list(list_string)

# hdf_filter_dict = {
#     'pick_bowl_location_similar_to_target': sampled_small_spatial_range_demos,
#     'pick_bowl_location_': sampled_large_spatial_range_demos
# }

# with open('droid_filter_dict_bowl_pick_place.pkl', 'wb') as f:
#     pickle.dump(hdf_filter_dict, f)
# print()


# print()