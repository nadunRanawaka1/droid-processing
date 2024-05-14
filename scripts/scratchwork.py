import pickle
import nexusformat.nexus as nx


demo_fn = "/media/nadun/Data/Droid/droid_hdf5/droid_100.hdf5"

demo_file = nx.nxload(demo_fn)
print(demo_file.tree)



