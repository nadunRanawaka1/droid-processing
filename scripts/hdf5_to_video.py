import cv2
from PIL import Image
import os
import h5py
import nexusformat.nexus as nx


demo_fn = "/nethome/nkra3/robomimic-v2/datasets/retriever/put_can_in_box/cotraining_datasets/spatial_retrieved.hdf5"

CAMERA_NAME = "shoulderview_left_image" # can change this
OUTPUT_FOLDER_NAME = "/nethome/nkra3/robomimic-v2/videos/retriever/put_can_in_box"
VIDEO_NAME = "spatial_retrieved_can_2"

video_folder = OUTPUT_FOLDER_NAME
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

### Uncomment below if you'd like to see the structure of the .hdf5 file

# demo_file = nx.nxload(demo_fn)
# print(demo_file.tree)

demo_file = h5py.File(demo_fn, 'r')
demos = demo_file['data']

video_list = []
fps = 20

for j, demo in enumerate(demos):
    print(f"Processing demo: {j}")

    if (demo != "mask"):
        view = demos[demo]['obs'][f'{CAMERA_NAME}']
        image_list = []
        for i in range(view.shape[0]):
            video_list.append(cv2.cvtColor(view[i], cv2.COLOR_RGB2BGR))
            

video_fn = os.path.join(video_folder, f"{VIDEO_NAME}.mp4")
width = video_list[1].shape[0]
height = video_list[1].shape[1]

video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))
for i in range(len(video_list)):
    video_writer.write(video_list[i])
video_writer.release()
