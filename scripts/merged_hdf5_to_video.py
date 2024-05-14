import cv2
from PIL import Image
import os
import h5py
import nexusformat.nexus as nx

demo_fn = "/media/nadun/Data/Droid/droid_hdf5/droid_exp_datasets/droid_mixed_agentview.hdf5"
video_folder = "/media/nadun/Data/Droid/droid_hdf5" #Destination

CAMERA_NAME = "agentview"
OUTPUT_FOLDER_NAME = "/media/nadun/Data/Droid/droid_hdf5/droid_exp_datasets"

video_folder = os.path.join(video_folder,OUTPUT_FOLDER_NAME)
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

demo_file = h5py.File(demo_fn)

# actions = demo_file['data']['demo_0']['additional_data']['controller_info']['robot_controls']['action']
demos = demo_file['data']

big_video_list = []
fps = 20

for j, demo in enumerate(demos):
    print(f"Processing demo: {j}")
    if (demo != "mask"):
        view = demos[demo]['obs'][f'{CAMERA_NAME}']
        image_list = []
        for i in range(view.shape[0]):
            # image_list.append(cv2.cvtColor(view[i], cv2.COLOR_RGB2BGR))
            big_video_list.append(cv2.cvtColor(view[i], cv2.COLOR_RGB2BGR))
            # image_list.append(cv2.applyColorMap(cv2.convertScaleAbs(view[i], alpha=0.03), cv2.COLORMAP_JET)) #for depth images

        # width = image_list[1].shape[0]
        # height = image_list[1].shape[1]

        # video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
        # for i in range(len(image_list)):
        #     video_writer.write(image_list[i])
        # video_writer.release()

video_fn = os.path.join(video_folder,f"{CAMERA_NAME}_all_demos.mp4")
width = big_video_list[1].shape[0]
height = big_video_list[1].shape[1]

video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
for i in range(len(big_video_list)):
    video_writer.write(big_video_list[i])
video_writer.release()
