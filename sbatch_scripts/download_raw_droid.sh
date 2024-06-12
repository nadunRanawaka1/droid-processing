#!/bin/bash
#SBATCH --job-name=download_raw_droid
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/download_raw_droid.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/download_raw_droid.err
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

cd /coc/flash7/nkra3/Droid/droid_raw

gsutil -m cp -r gs://gresearch/robotics/droid_raw/1.0.1/RAIL/success ./

