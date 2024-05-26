import h5py
import tensorflow_datasets as tfds
import numpy as np
import time
import datetime
from PIL import Image
import argparse



RESIZE_SHAPE = (128, 128)
def center_crop(im, t_h, t_w):
    assert(im.shape[-3] >= t_h and im.shape[-2] >= t_w)
    assert(im.shape[-1] in [1, 3])
    crop_h = int((im.shape[-3] - t_h) / 2)
    crop_w = int((im.shape[-2] - t_w) / 2)
    return im[..., crop_h:crop_h + t_h, crop_w:crop_w + t_w, :]


def resize_rgb_images_list(images, output_shape):
    """
    @param images: batch of images of shape (b,h,w,c)
    @param output_shape: tuple of (h',w') to resize to
    @return: resized batch of images after center cropping

    """
    image_list = []
    crop_size = min(images[0].shape[0], images[0].shape[1])
    for i in range(images.shape[0]):
        cropped_image = center_crop(images[i], crop_size, crop_size)
        resized_image = Image.fromarray(cropped_image).resize(output_shape, Image.BILINEAR)
        image_list.append(resized_image)

    images = np.stack(image_list, axis=0)
    return images

def resize_rgb_image(image, output_shape=RESIZE_SHAPE):
    """

    :param image: single rgb image
    :param output_shape: tuple of (h',w') to resize to
    :return: resized image after center cropping
    """

    crop_size = min(image.shape[0], image.shape[1])
    cropped_image = center_crop(image, crop_size, crop_size)
    resized_image = Image.fromarray(cropped_image).resize(output_shape, Image.BILINEAR)

    return resized_image

def droid_to_hdf5(droid_path, dst_hdf5_path):
    droid_ds = tfds.load("droid", data_dir=droid_path, split="train")
    counter = 0
    start = time.time()
    with h5py.File(f"{dst_hdf5_path}/droid.hdf5", "w") as f_dst:
        f_dst_grp = f_dst.create_group("data")
        num_written = 0
        total_samples = 0
        for episode in droid_ds:
            counter += 1
            if (counter % 100) == 0:
                print(f"Processed episode: {counter}")
                print(f"Time elapsed: {time.time() - start}")

            episode_metadata = episode["episode_metadata"]
            rec_folder = episode_metadata["recording_folderpath"].numpy().decode("utf-8")
            filepath = episode_metadata["file_path"].numpy().decode("utf-8")
            lang1, lang2, lang3 = None, None, None

            for step in episode["steps"]:
                lang1 = step["language_instruction"].numpy().decode("utf-8")
                lang2 = step["language_instruction_2"].numpy().decode("utf-8")
                lang3 = step["language_instruction_3"].numpy().decode("utf-8")
                break

            # Create destination group and add demo metadata
            dst_grp = f_dst_grp.create_group("demo_{}".format(num_written))
            dst_grp.attrs["recording_folderpath"] = rec_folder
            dst_grp.attrs["filepath"] = filepath
            dst_grp.attrs["language_instruction_1"] = lang1
            dst_grp.attrs["language_instruction_2"] = lang2
            dst_grp.attrs["language_instruction_3"] = lang3

            #Create lists for all other data in episode
            is_first = []
            is_last = []
            is_terminal = []

            obs_gripper_position = []
            obs_cartesian_position = []
            obs_joint_position = []
            wrist_image_left = []
            exterior_image_1_left = []
            exterior_image_2_left = []

            gripper_position_action, gripper_velocity_action, cartesian_position_action = [], [], []
            cartesian_velocity_action, joint_position_action, joint_velocity_action = [], [], []

            discount = []
            reward = []
            action = []

            step_counter = 0
            for step in episode["steps"]:
                step_counter += 1
                total_samples += 1

                is_first.append(step["is_first"].numpy())
                is_last.append(step["is_last"].numpy())
                is_terminal.append(step["is_terminal"].numpy())

                obs_gripper_position.append(step["observation"]["gripper_position"].numpy())
                obs_cartesian_position.append(step["observation"]["cartesian_position"].numpy())
                obs_joint_position.append(step["observation"]["joint_position"].numpy())


                ### Resize and append images
                w_img = resize_rgb_image(step["observation"]["wrist_image_left"].numpy())
                e_img_1 = resize_rgb_image(step["observation"]["exterior_image_1_left"].numpy())
                e_img_2 = resize_rgb_image(step["observation"]["exterior_image_2_left"].numpy())

                wrist_image_left.append(w_img)
                exterior_image_1_left.append(e_img_1)
                exterior_image_2_left.append(e_img_2)

                # Parse actions
                gripper_position_action.append(step["action_dict"]["gripper_position"].numpy())
                gripper_velocity_action.append(step["action_dict"]["gripper_velocity"].numpy())
                cartesian_position_action.append(step["action_dict"]["cartesian_position"].numpy())
                cartesian_velocity_action.append(step["action_dict"]["cartesian_velocity"].numpy())
                joint_position_action.append(step["action_dict"]["joint_position"].numpy())
                joint_velocity_action.append(step["action_dict"]["joint_velocity"].numpy())

                # Finally
                discount.append(step["discount"].numpy())
                reward.append(step["reward"].numpy())
                action.append(step["action"].numpy())


            ### Turn everything into a numpy array
            is_first = np.array(is_first)
            is_last = np.array(is_last)
            is_terminal = np.array(is_terminal)

            obs_dict = {"gripper_position": np.stack(obs_gripper_position,axis=0),
                        "cartesian_position": np.stack(obs_cartesian_position, axis=0),
                        "joint_position": np.stack(obs_joint_position, axis=0),
                        "wrist_image_left":np.stack(wrist_image_left, axis=0),
                        "exterior_image_1_left":np.stack(exterior_image_1_left, axis=0),
                        "exterior_image_2_left": np.stack(exterior_image_2_left, axis=0)}

            action_list = [gripper_position_action, gripper_velocity_action, cartesian_position_action,
                            cartesian_velocity_action, joint_position_action, joint_velocity_action]

            for i, action_type in enumerate(action_list):
                action_list[i] = np.stack(action_type, axis=0)

            # Finally
            discount = np.array(discount)
            reward = np.array(reward)
            action = np.stack(action, axis=0)

            # Add everything to hdf5 file
            dst_grp.create_dataset("is_first", data=np.array(is_first))
            dst_grp.create_dataset("is_last", data=np.array(is_last))
            dst_grp.create_dataset("is_terminal", data=np.array(is_terminal))

            # Adding obs
            for k in obs_dict:
                dst_grp.create_dataset("obs/{}".format(k), data=np.array(obs_dict[k][:]))

            # Adding actions
            dst_grp.create_dataset("gripper_position_action", data=np.array(gripper_position_action[:]))
            dst_grp.create_dataset("gripper_velocity_action", data=np.array(gripper_velocity_action[:]))
            dst_grp.create_dataset("cartesian_position_action", data=np.array(cartesian_position_action[:]))
            dst_grp.create_dataset("cartesian_velocity_action", data=np.array(cartesian_velocity_action[:]))
            dst_grp.create_dataset("joint_position_action", data=np.array(joint_position_action[:]))
            dst_grp.create_dataset("joint_velocity_action", data=np.array(joint_velocity_action[:]))

            # Finally
            dst_grp.create_dataset("discount", data=np.array(discount[:]))
            dst_grp.create_dataset("reward", data=np.array(reward[:]))
            dst_grp.create_dataset("action", data=np.array(action[:]))

            dst_grp.attrs["num_samples"] = step_counter

            num_written += 1

        f_dst_grp.attrs["total"] = total_samples
    total_seconds = time.time() - start
    print(f"Total time taken to convert droid: {datetime.timedelta(seconds=total_seconds)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_dir",
                        type=str,
                        required=True,
                        help="path to directory where droid dataset is saved")

    parser.add_argument("--save_dir",
                        type=str,
                        required=True,
                        help="directory to save the droid dataset in hdf5 format")

    args = parser.parse_args()

    droid_to_hdf5(args.dataset_dir, args.save_dir)

