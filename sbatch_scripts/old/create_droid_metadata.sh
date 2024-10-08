#!/bin/bash
#SBATCH --job-name=create_droid_metadata_new
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/create_droid_metadata_new.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/create_droid_metadata_new.err
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

srun -u python -u scripts/create_metadata_from_hdf5.py --droid_path="/nethome/nkra3/flash7/Droid/droid_hdf5/droid.hdf5" --save_dir="/nethome/nkra3/flash7/Droid/droid_hdf5/metadata"