import tensorflow_datasets as tfds


droid_path = "/srv/rl2-lab/flash7/vsaxena33/work/robomimicV2/datasets/droid/droid/1.0.0"
builder = tfds.builder_from_directory(builder_dir=droid_path)
print(builder.info.features)


