import cv2
from PIL import Image
import os
import h5py
import nexusformat.nexus as nx
import pickle
import pandas as pd
import numpy as np

demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/place_bowl_on_plate/place_bowl_on_plate_vary_both_locations_big_demo_selected_agentview.hdf5"
demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

demo_file = h5py.File(demo_fn, 'r')

metadata_path = "/nethome/nkra3/flash7/Droid/droid-processing/scripts/place_bowl_on_plate_spatial_metrics.pkl"
df = pd.read_pickle(metadata_path)



OUTPUT_FOLDER_NAME = "/nethome/nkra3/flash7/Droid/droid_hdf5/videos"

if not os.path.exists(OUTPUT_FOLDER_NAME):
    os.makedirs(OUTPUT_FOLDER_NAME)


demos = demo_file['data']

big_video_list = []
fps = 20

for j, demo in enumerate(demos):


    if demo not in df["Demo"].values:
        continue
    print(f"Processing demo: {demo}")
    demo_metadata = df[df['Demo'] == demo]

    pick_skill_timesteps = demo_metadata["pick_skill_timestep_ranges"].tolist()[0][0]
    pick_skill_timesteps = range(pick_skill_timesteps[0], pick_skill_timesteps[1])

    place_skill_timesteps = demo_metadata["place_skill_timestep_ranges"].tolist()[0][0]
    place_skill_timesteps = range(place_skill_timesteps[0], place_skill_timesteps[1])

    images = demos[demo]["obs/shoulderview_left_image"]

    for i in range(images.shape[0]):
        image = images[i]
        if i in pick_skill_timesteps:
            caption = f"{demo}.              Skill: Pick"
        elif i in place_skill_timesteps:
            caption = f"{demo}.              Skill : Place"
        else:
            caption = f"{demo}.              Skill : None"

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if len(caption) > 25:
            image = cv2.putText(img=np.copy(image), text=caption[:20], org = (10, 10), fontFace=1, fontScale=1, color=(255,255,255), thickness=1)
            image = cv2.putText(img=np.copy(image), text=caption[20:], org=(10, 30), fontFace=1, fontScale=1,
                                color=(255, 255, 255), thickness=1)
        else:
            image = cv2.putText(img=np.copy(image), text=caption, org=(10, 10), fontFace=1, fontScale=1,
                                color=(255, 255 , 255), thickness=1)
        big_video_list.append(image)

    # print(demo_num)




### Generating video

video_fn = os.path.join(OUTPUT_FOLDER_NAME,f"pick_place_bowl_pick_and_place_annotated.mp4")
width = big_video_list[1].shape[0]
height = big_video_list[1].shape[1]

video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
for i in range(len(big_video_list)):
    video_writer.write(big_video_list[i])
video_writer.release()


print()

