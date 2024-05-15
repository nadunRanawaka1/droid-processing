import h5py
import numpy as np
import argparse
from torchvision.utils import make_grid
import torchvision
import torch
from robomimic.utils.obs_utils import batch_image_hwc_to_chw

def create_cam_grids(cam1_path, cam2_path, savedir):

    cam1_list  = []
    cam2_list = []

    cam1_data = h5py.File(cam1_path)['data']
    cam2_data = h5py.File(cam2_path)['data']

    for demo in cam1_data:
        demo_cam1 = cam1_data[demo]
        demo_cam2 = cam2_data[demo]

        cam1_image = demo_cam1["obs/agentview"][0]
        cam2_image = demo_cam2["obs/agentview"][0]

        cam1_list.append(torch.from_numpy(cam1_image))
        cam2_list.append(torch.from_numpy(cam2_image))

    cam1_list = torch.stack(cam1_list)
    cam2_list = torch.stack(cam2_list)

    cam1_list = batch_image_hwc_to_chw(cam1_list)
    cam2_list = batch_image_hwc_to_chw(cam2_list)

    grid_cam_1 = make_grid(cam1_list, padding=25)
    grid_cam_2 = make_grid(cam2_list, padding=25)

    grid_cam_1_img = torchvision.transforms.ToPILImage()(grid_cam_1)
    grid_cam_2_img = torchvision.transforms.ToPILImage()(grid_cam_2)

    grid_cam_1_img.save(f"{savedir}/cam1_grid.png")
    grid_cam_2_img.save(f"{savedir}/cam2_grid.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--cam1_path",
                        type=str,
                        required=True,
                        help="path to droid")

    parser.add_argument("--cam2_path",
                        type=str,
                        required=True,
                        help="path to droid")


    parser.add_argument("--save_dir",
                        type=str,
                        required=True,
                        help="where to save the cam images")

    args = parser.parse_args()

    cam1_path = args.cam1_path
    cam2_path = args.cam2_path

    save_dir = args.save_dir

    create_cam_grids(cam1_path, cam2_path, save_dir)


