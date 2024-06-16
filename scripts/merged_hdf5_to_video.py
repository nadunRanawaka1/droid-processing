import cv2
from PIL import Image
import os
import h5py
import nexusformat.nexus as nx

demo_fn = "/nethome/nkra3/flash7/Droid/droid_hdf5/exp_datasets/single_task_datasets/Put_the_marker_in_the_cup_demos.hdf5"
# video_folder = "/media/nadun/Data/Droid/droid_hdf5" #Destination

CAMERA_NAME = "shoulderview_left_image"
OUTPUT_FOLDER_NAME = "/nethome/nkra3/flash7/Droid/droid_hdf5/videos"

video_folder = OUTPUT_FOLDER_NAME
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

demo_file = h5py.File(demo_fn)

demos = demo_file['data']

big_video_list = []
fps = 20

for j, demo in enumerate(demos):
    print(f"Processing demo: {j}")
    if (demo != "mask"):
        view = demos[demo]['obs'][f'{CAMERA_NAME}']
        image_list = []
        for i in range(view.shape[0]):
            big_video_list.append(cv2.cvtColor(view[i], cv2.COLOR_RGB2BGR))
            

video_fn = os.path.join(video_folder,f"put_marker_in_cup_{CAMERA_NAME}_all_demos.mp4")
width = big_video_list[1].shape[0]
height = big_video_list[1].shape[1]

video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
for i in range(len(big_video_list)):
    video_writer.write(big_video_list[i])
video_writer.release()
