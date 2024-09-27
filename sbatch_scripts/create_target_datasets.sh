#!/bin/bash
#SBATCH --job-name=create_target_datasets
#SBATCH --output=/nethome/nkra3/flash7/logs/sbatch_out/droid_processing/retriever/create_target_datasets.out
#SBATCH --error=/nethome/nkra3/flash7/logs/sbatch_err/droid_processing/retriever/create_target_datasets.err
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
srun -u python -u scripts/create_target_dataset.py 