import pandas as pd
import pickle

metadata_fp = "/media/nadun/Data/Droid/droid_hdf5/metadata/all_droid_metadata.pkl"

df = pd.read_pickle(metadata_fp)

kitchen_df = df[df['building'].str.contains('kitchen', case=False, na=False)]

first_demo_per_kitchen = kitchen_df.drop_duplicates(subset='scene_id', keep='first')
demo_names = first_demo_per_kitchen['Demo']
demo_names = demo_names.tolist()

with open("/media/nadun/Data/Droid/droid_hdf5/metadata/demos_with_kitchens.pkl", "wb") as f:
    pickle.dump(demo_names, f)

print()