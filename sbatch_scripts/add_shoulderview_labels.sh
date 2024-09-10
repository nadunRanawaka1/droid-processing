#!/bin/bash
#SBATCH --job-name=droid_add_shoulderview_labels
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/droid_add_shoulderview_labels.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing/droid_add_shoulderview_labels.err
#SBATCH --partition=rl2-lab
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --exclude="clippy"


export PYTHONUNBUFFERED=TRUE
source ~/.bashrc
source /nethome/nkra3/flash7/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate droid-processing

cd /coc/flash7/nkra3/Droid/droid-processing
srun -u python -u scripts/add_shoulderview_labels_to_droid.py 