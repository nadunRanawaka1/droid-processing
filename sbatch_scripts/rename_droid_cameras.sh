#!/bin/bash
#SBATCH --job-name=rename_droid_cameras
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/rename_droid_cameras.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/rename_droid_cameras.err
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
srun -u python -u scripts/rename_droid_cameras.py --droid_path="/nethome/nkra3/flash7/Droid/droid_hdf5/droid.hdf5"