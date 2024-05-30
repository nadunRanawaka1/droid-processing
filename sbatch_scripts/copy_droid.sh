#!/bin/bash
#SBATCH --job-name=copy_droid
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/copy_droid.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing/copy_droid.err
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

cd /coc/flash7/nkra3/Droid/droid_hdf5
rsync -ah droid.hdf5 original_datasets/
