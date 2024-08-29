import cv2
from PIL import Image
import os
import h5py
import nexusformat.nexus as nx


demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/kitchen/put_screwdriver_in_drawer/obj_tex_datasets/red+blue+yellow.hdf5"
# video_folder = "/media/nadun/Data/Droid/droid_hdf5" #Destination

# CAMERA_NAME = "selected_agentview_image"
CAMERA_NAME = "shoulderview_right_image"
OUTPUT_FOLDER_NAME = "/nethome/nkra3/flash7/Droid/droid_hdf5/videos/put_screw_driver_in_drawer/obj_tex"

video_folder = OUTPUT_FOLDER_NAME
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)

demo_file = h5py.File(demo_fn, 'r')

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
            

video_fn = os.path.join(video_folder,f"RBY.mp4")
width = big_video_list[1].shape[0]
height = big_video_list[1].shape[1]

video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
for i in range(len(big_video_list)):
    video_writer.write(big_video_list[i])
video_writer.release()
