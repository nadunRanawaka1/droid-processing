#!/bin/bash
#SBATCH --job-name=droid_add_lang_emb
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/droid_add_lang_emb.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing/droid_add_lang_emb.err
#SBATCH --partition=rl2-lab
#SBATCH --gpus-per-node="a40:1"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --exclude="clippy"
#SBATCH --mem-per-gpu=80G


export PYTHONUNBUFFERED=TRUE
source ~/.bashrc
source /nethome/nkra3/flash7/miniconda3/etc/profile.d/conda.sh
conda deactivate
conda activate droid

cd /coc/flash7/nkra3/Droid/droid-processing
srun -u python -u scripts/add_lang_emb_to_droid.py 