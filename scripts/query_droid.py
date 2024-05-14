import tensorflow_datasets as tfds
import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
import cv2

ds = tfds.load("droid_100", data_dir="/media/nadun/Data/Droid", split="train")

selected_language_instructions = set()
query_terms = ["put", "pick"]

print(type(ds))

selected_episodes = []

for episode in ds:
    for step in episode["steps"]:
        lang_1 = step["language_instruction"].numpy().decode("utf-8")
        lang_2 = step["language_instruction_2"].numpy().decode("utf-8")
        lang_3 = step["language_instruction_3"].numpy().decode("utf-8")
        if (any(term in lang_1 for term in query_terms) or
            any(term in lang_2 for term in query_terms) or any(term in lang_3 for term in query_terms)):
            selected_episodes.append(episode)
            selected_language_instructions.update([lang_1, lang_2, lang_3])
        break


#Below for visualizing
video_fn = "selected_demos.mp4"
width = 180
height = 320
fps = 15
video_writer = cv2.VideoWriter(video_fn, cv2.VideoWriter_fourcc(*'mp4v'), fps, (height, width))

for episode in selected_episodes:
    images_ext_1, images_ext_2, images_wrist = [], [], []
    for step in episode['steps']:
        image = cv2.cvtColor(step['observation']['exterior_image_1_left'].numpy(), cv2.COLOR_RGB2BGR)
        caption = step['language_instruction'].numpy().decode()
        if len(caption) > 25:
            image = cv2.putText(img=np.copy(image), text=caption[:25], org = (10, 10), fontFace=1, fontScale=1, color=(255,255,255), thickness=1)
            image = cv2.putText(img=np.copy(image), text=caption[25:], org=(10, 20), fontFace=1, fontScale=1,
                                color=(255, 255, 255), thickness=1)
        else:
            image = cv2.putText(img=np.copy(image), text=caption, org=(10, 10), fontFace=1, fontScale=1,
                                color=(255, 255 , 255), thickness=1)
        video_writer.write(image)


video_writer.release()

print("Generated video")
