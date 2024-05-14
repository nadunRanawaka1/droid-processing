import h5py
import numpy as np
import argparse
import matplotlib.pyplot as plt
import math

PLACE_TERMS = ["put", "place"]

def create_droid_cam_views(droid_hdf_path, save_path):
    droid = h5py.File(droid_hdf_path)
    droid = droid['data']
    counter = 1000
    demo_list = []
    for demo in droid:
        demo = droid[demo]
        lang_1 = demo.attrs["language_instruction_1"]
        lang_2 = demo.attrs["language_instruction_2"]
        lang_3 = demo.attrs["language_instruction_3"]
        
        if "pick" in lang_1 or "pick" in lang_2 or "pick" in lang_3:
            if (any(term in lang_1 for term in PLACE_TERMS) or
                    any(term in lang_2 for term in PLACE_TERMS) or any(term in lang_3 for term in PLACE_TERMS)):
                demo_list.append((demo.name, demo['action'].shape[0]))
                counter -= 1
        if counter == 0:
            break
    demo_list = sorted(demo_list, key=lambda tup:tup[1])

    # Create hdf5 files for saving
    cam_1_renamed_file = h5py.File(f"{save_path}/droid_cam_1_agentview.hdf5", "w")
    cam_2_renamed_file = h5py.File(f"{save_path}/droid_cam_2_agentview.hdf5", "w")
    mixed_renamed_file = h5py.File(f"{save_path}/droid_mixed_agentview.hdf5", "w")

    cam_1_renamed_data = cam_1_renamed_file.create_group("data")
    cam_2_renamed_data = cam_2_renamed_file.create_group("data")
    mixed_renamed_data  = mixed_renamed_file.create_group("data")

    demo_num = 0

    last_mix_cam_1 = False

    # Create grids of initial cam 1 and cam 2 views of each demo
    total_selected_demos = len(demo_list)
    grid_size = math.ceil(math.sqrt(total_selected_demos))
    cam1_fig, cam1_ax = plt.subplots(nrows=grid_size, ncols=grid_size)
    cam2_fig, cam2_ax = plt.subplots(nrows=grid_size, ncols=grid_size)

    for demo in demo_list:
        demo, _ = demo
        demo_data = droid[demo]

        # Copy first image of cam 1 and cam 2 to grid for debugging
        x = demo_num % grid_size
        y = demo_num // grid_size

        cam1_ax[x, y].imshow(demo_data["obs/exterior_image_1_left"][0])
        cam2_ax[x, y].imshow(demo_data["obs/exterior_image_2_left"][0])

        # First set cam 1 as the agentview
        demo_data.copy(demo_data, cam_1_renamed_data, name=f"demo_{demo_num}")
        cam_1_renamed_data.create_dataset(f"demo_{demo_num}/obs/agentview",  data= demo_data["obs/exterior_image_1_left"])

        # Next set cam 2 as agentview and copy
        demo_data.copy(demo_data, cam_2_renamed_data, name=f"demo_{demo_num}")
        cam_2_renamed_data.create_dataset(f"demo_{demo_num}/obs/agentview", data= demo_data["obs/exterior_image_2_left"])

        # Next set the mixed
        if last_mix_cam_1: # if the previous demo had cam 1 set as agentview, for this demo, set cam 2
            demo_data.copy(demo_data, mixed_renamed_data, name=f"demo_{demo_num}")
            mixed_renamed_data.create_dataset(f"demo_{demo_num}/obs/agentview", data=demo_data["obs/exterior_image_2_left"])
        else:
            demo_data.copy(demo_data, mixed_renamed_data, name=f"demo_{demo_num}")
            mixed_renamed_data.create_dataset(f"demo_{demo_num}/obs/agentview", data=demo_data["obs/exterior_image_1_left"])

        last_mix_cam_1 = ~last_mix_cam_1
        demo_num += 1
    cam_1_renamed_file.close()
    cam_2_renamed_file.close()
    mixed_renamed_file.close()

    cam1_fig.savefig(f"{save_path}/Cam1_grid.jpg")
    cam2_fig.savefig(f"{save_path}/Cam2_grid.jpg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--droid_path",
                        type=str,
                        required=True,
                        help="path to droid")

    parser.add_argument("--save_dir",
                        type=str,
                        required=True,
                        help="where to save the split droid datasets")

    args = parser.parse_args()

    create_droid_cam_views(args.droid_path, args.save_dir)


