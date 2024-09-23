'''
Borrowed from droid_policy_learning
https://github.com/droid-dataset/droid_policy_learning
'''

import os
import time

import h5py
import nexusformat.nexus as nx
import torch
import json
import argparse




def add_lang(path, raw_lang=None):

    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModel.from_pretrained("distilbert-base-uncased", torch_dtype=torch.float16)
    model.to('cuda')

    start = time.time()
    dataset = h5py.File(path, 'a')
    dataset_grp = dataset['data']

    env_args = json.loads(dataset_grp.attrs['env_args'])

    if raw_lang is None:
        raw_lang = env_args['lang']
    else:
        env_args['lang'] = raw_lang
        dataset_grp.attrs['env_args'] = json.dumps(env_args)

    print(f"This is the lang emb for the dataset: {raw_lang}")

    num_written = 0

    for demo in dataset_grp:
        demo_grp = dataset_grp[demo]
        obs = demo_grp['obs']

        if (num_written % 10) == 0:
            print(f"Processing demo: {num_written}. Time elapsed: {time.time() - start}")

        num_written += 1

        # raw_lang = demo_grp.attrs['language_instruction_1']

        if "language_raw" in obs:
            del obs['language_raw']
        if "language_distilbert" in obs:
            del obs['language_distilbert']

        H = demo_grp['absolute_actions'].shape[0]
        encoded_input = tokenizer(raw_lang, return_tensors='pt').to('cuda')
        outputs = model(**encoded_input)
        encoded_lang = outputs.last_hidden_state.sum(1).squeeze().unsqueeze(0).repeat(H, 1)

        obs.create_dataset("language_raw", data=[raw_lang]*H)
        obs.create_dataset("language_distilbert", data=encoded_lang.cpu().detach().numpy())

    dataset.close()

    print("COMPLETED ADD LANGUAGE EMBEDDING TO RL2 DATASET")



    # Extract language data
    # if "lang_fixed" not in f["observation"]:
    #     f["observation"].create_group("lang_fixed")
    # lang_grp = f["observation/lang_fixed"]
    #
    #
    # if "language_raw" not in f["observation/lang_fixed"]:
    #     lang_grp.create_dataset("language_raw", data=[raw_lang]*H)
    #     lang_grp.create_dataset("language_distilbert", data=encoded_lang.cpu().detach().numpy())
    # else:
    #     f["observation/lang_fixed/language_raw"][...] = [raw_lang]*H
    #     f["observation/lang_fixed/language_distilbert"][...] = encoded_lang.cpu().detach().numpy()
    # f.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_path",
                        type=str,
                        required=True,
                        default=None,
                        help="path to rl2 dataset to add lang to")
    
    parser.add_argument("--raw_lang",
                        type=str,
                        default=None,
                        )

    # dataset_path = "/nethome/nkra3/robomimic-v2/datasets/retriever/put_can_in_box/target_datasets/20_target_dataset_with_lang.hdf5"

    args = parser.parse_args()
    add_lang(args.dataset_path, args.raw_lang)

