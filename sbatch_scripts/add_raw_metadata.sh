#!/bin/bash
#SBATCH --job-name=add_droid_metadata
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/add_droid_metadata.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing/add_droid_metadata.err
#SBATCH --partition=rl2-lab
#SBATCH --time 96:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --qos="long"
#SBATCH --exclude="clippy"


export PYTHONUNBUFFERED=TRUE
source ~/.bashrc
source /nethome/nkra3/flash7/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate droid

cd /coc/flash7/nkra3/Droid/droid-processing

srun -u python -u scripts/add_raw_metadata.py