import tensorflow_datasets as tfds


droid_path = "/media/nadun/Data/Droid"

droid_ds = tfds.load("droid_100", data_dir=droid_path, split="train")

for episode in droid_ds:
    for step in episode['steps']:
        obs = step['observation']
        print(obs['exterior_image_1_left'])
        print()
    print()
    break


