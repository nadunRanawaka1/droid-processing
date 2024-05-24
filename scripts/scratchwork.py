import pickle
import nexusformat.nexus as nx
import h5py


demo_fn = "/nethome/nkra3/flash7/Droid/robomimic-dev/datasets/place_bowl_on_plate/place_bowl_on_plate_vary_bowl_location_big_10_demos_demo.hdf5"

# demo_file = nx.nxload(demo_fn)
# print(demo_file.tree)

demo_file = h5py.File(demo_fn)

masks = demo_file['mask']
print(masks['pick_place_large_spatial'][:])
print(masks['pick_place_small_spatial'][:])

demo_file.close()


