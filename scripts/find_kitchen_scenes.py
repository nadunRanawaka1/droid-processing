import pandas as pd
import pickle
import h5py
import imageio

# metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/all_droid_metadata.pkl"

# df = pd.read_pickle(metadata_fp)

# kitchen_df = df[df['building'].str.contains('kitchen', case=False, na=False)]

# first_demo_per_kitchen = kitchen_df.drop_duplicates(subset='scene_id', keep='first')
# demo_names = first_demo_per_kitchen['Demo']
# demo_names = demo_names.tolist()

# with open("/media/nadun/Data/Droid/droid_hdf5/metadata/demos_with_kitchens.pkl", "wb") as f:
#     pickle.dump(demo_names, f)

# print()

demo_names_fn = "/nethome/nkra3/flash7/Droid/droid_hdf5/metadata/raw_metadata/demos_with_kitchens.pkl"

with open(demo_names_fn, "rb") as f:
    demo_names = pickle.load(f)

print(demo_names)

droid_fn = "/nethome/nkra3/flash7/Droid/droid_hdf5/droid.hdf5"
droid_file = h5py.File(droid_fn, 'r')
droid = droid_file['data']

video_writer = imageio.get_writer("/nethome/nkra3/flash7/Droid/droid_hdf5/videos/kitchen_demos/demo_videos_4x.mp4", fps=60)

for demo in demo_names:
    print(f"Processing demo: {demo}")
    demo = droid[demo]
    images = demo['obs/exterior_image_2_left'][:]

    for i in range(images.shape[0]):
        video_writer.append_data(images[i])

video_writer.close()
