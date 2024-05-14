import tensorflow_datasets as tfds
import numpy as np
import time
import pickle
import argparse

ds = tfds.load("droid_100", data_dir="/media/nadun/Data/Droid", split="train")

all_language_instructions = set()
counter = 0

start = time.time()
for episode in ds:
    counter += 1
    if (counter % 1000) == 0:
        print(f"Processed episode: {counter}")
    for step in episode["steps"]:
        lang_1 = step["language_instruction"].numpy().decode("utf-8")
        lang_2 = step["language_instruction_2"].numpy().decode("utf-8")
        lang_3 = step["language_instruction_3"].numpy().decode("utf-8")
        all_language_instructions.update([lang_1, lang_2, lang_3])
        break
time_taken = time.time() - start
print(f"Total time taken: {time_taken}" )

with open("all_language_instructions_extended", 'wb') as f:
    pickle.dump(all_language_instructions, f)
print()