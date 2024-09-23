#!/bin/bash
#SBATCH --job-name=rl2_add_lang_emb
#SBATCH --output=/coc/flash7/nkra3/logs/sbatch_out/droid_processing/rl2_add_lang_emb.out
#SBATCH --error=/coc/flash7/nkra3/logs/sbatch_err/droid_processing/rl2_add_lang_emb.err
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
srun -u python -u scripts/add_lang_emb_to_rl2.py --raw_lang='put the can in the box' \
 --dataset_path=/nethome/nkra3/robomimic-v2/datasets/retriever/put_can_in_box/target_datasets/50_target_dataset.hdf5