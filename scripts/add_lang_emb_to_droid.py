'''
Borrowed from droid_policy_learning
https://github.com/droid-dataset/droid_policy_learning
'''

import os
import time

import h5py
import nexusformat.nexus as nx
import torch

from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModel.from_pretrained("distilbert-base-uncased", torch_dtype=torch.float16)
model.to('cuda')


def add_lang(path):

    start = time.time()
    droid = h5py.File(path, 'a')
    droid_data = droid['data']

    num_written = 0

    for demo in droid_data:
        demo_grp = droid_data[demo]
        obs = demo_grp['obs']

        if (num_written % 1000) == 0:
            print(f"Processing demo: {num_written}. Time elapsed: {time.time() - start}")

        num_written += 1

        raw_lang = demo_grp.attrs['language_instruction_1']

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

    droid.close()



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



droid_path = "/media/nadun/Data/Droid/droid_hdf5/droid_100.hdf5"

add_lang(droid_path)

