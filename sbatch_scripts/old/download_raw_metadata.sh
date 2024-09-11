#!/bin/bash
#SBATCH --job-name=download_droid_raw_metadata
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/download_droid_raw_metadata.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/download_droid_raw_metadata.err
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

cd /nethome/nkra3/flash7/Droid/droid_hdf5/metadata/raw_metadata

cat metadata_files.txt | xargs -n 50 -P 10 -I {} gsutil -m cp {} raw_metadata_files/
