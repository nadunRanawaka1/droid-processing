#!/bin/bash
#SBATCH --job-name=create_grid_images
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/create_grid_images.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/create_grid_images.err
#SBATCH --partition=rl2-lab
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --exclude="clippy"


export PYTHONUNBUFFERED=TRUE
source ~/.bashrc
source /nethome/nkra3/flash7/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate droid

cd /coc/flash7/nkra3/Droid/droid-processing


srun -u python -u scripts/create_grid_of_initial_images.py --cam1_path="/coc/flash7/nkra3/Droid/droid_hdf5/exp_datasets/droid_cam_1_agentview.hdf5" --cam2_path="/coc/flash7/nkra3/Droid/droid_hdf5/exp_datasets/droid_cam_2_agentview.hdf5" --save_dir="/coc/flash7/nkra3/Droid/droid_hdf5/exp_datasets"

