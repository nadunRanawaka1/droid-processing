#!/bin/bash
#SBATCH --job-name=select_agentview_can
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/collector/select_agentview_can.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing//collector/select_agentview_can.err
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

srun -u python -u scripts/select_agentview_from_dataset.py \
 --dataset_path="/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/green_can_100_demos_demo.hdf5" \
 --target_path="/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/original_demos/green_can_campose_target_30_demos_demo.hdf5" \
 --processed_datasets_folder="/nethome/nkra3/robomimic-v2/datasets/collector/put_can_in_box/cam_pose_datasets"