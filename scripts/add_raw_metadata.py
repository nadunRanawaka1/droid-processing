import os
import pandas as pd
import json

metadata_fp = "/nethome/nkra3/flash7/Droid/droid_hdf5/metadata/droid_metadata.pkl"

df = pd.read_pickle(metadata_fp)

# Start defining new metadata
df["lab"] = pd.Series(dtype="str")
df["date"] = pd.Series(dtype="str")
df["timestamp"] = pd.Series(dtype="str")
df["scene_id"] = pd.Series(dtype="int")
df["task"] = pd.Series(dtype="str")
df["building"] = pd.Series(dtype="str")
df["trajectory_length"] = pd.Series(dtype="int")
df["wrist_cam_extrinsics"] = [[0.0 for i in range(7)] for j in range(len(df))]
df["ext1_cam_extrinsics"] = [[0.0 for i in range(7)] for j in range(len(df))]
df["ext2_cam_extrinsics"] = [[0.0 for i in range(7)] for j in range(len(df))]

metadata_file_dir = "/nethome/nkra3/flash7/Droid/droid_hdf5/metadata/raw_metadata/raw_metadata_files"

raw_metadata_file_names = os.listdir(metadata_file_dir)

counter = 0
for file in raw_metadata_file_names:
    fp = os.path.join(metadata_file_dir, file)
    if (counter % 100 == 0):
        print(f"Processed demo: {counter}")
    counter += 1
    with open(fp,) as f:
        metadata = json.load(f)

        hdf5_path = metadata['hdf5_path']
        demo_df = df[df['filepath'].str.contains(hdf5_path)]
        if not len(demo_df):
            continue
        index = demo_df['Demo'].index.values[0]

        df[df['filepath'].str.contains(hdf5_path)]["lab"] = metadata["lab"]
        df[df['filepath'].str.contains(hdf5_path)]["date"] = metadata["date"]
        df[df['filepath'].str.contains(hdf5_path)]["timestamp"] = metadata["timestamp"]
        df[df['filepath'].str.contains(hdf5_path)]["scene_id"] = metadata["scene_id"]
        df[df['filepath'].str.contains(hdf5_path)]["task"] = metadata["current_task"]
        df[df['filepath'].str.contains(hdf5_path)]["building"] = metadata["building"]
        df[df['filepath'].str.contains(hdf5_path)]["trajectory_length"] = metadata["trajectory_length"]
        df.at[index, "wrist_cam_extrinsics"] = metadata["wrist_cam_extrinsics"]
        df.at[index, "ext1_cam_extrinsics"] = metadata["ext1_cam_extrinsics"]
        df.at[index, "ext2_cam_extrinsics"] = metadata["ext2_cam_extrinsics"]


df.to_pickle("/nethome/nkra3/flash7/Droid/droid_hdf5/metadata/new_droid_metadata.pkl")


