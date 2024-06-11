import tensorflow_datasets as tfds


droid_path = "/media/nadun/Data/Droid/droid_100/1.0.0"
builder = tfds.builder_from_directory(builder_dir=droid_path)
print(builder.info.features)


