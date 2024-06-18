import os
import requests
import json
import yaml
import sys
import re

def read_species_file(filename):
    assert os.path.exists(filename), f'No such file {filename}'
    with open(filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
def read_json(filename):
    assert os.path.exists(filename), f'No such file {filename}'
    with open(filename, 'r') as f:
        jd = json.load(f)
        return jd
def dump_into_file(new_annos, new_json_file):
    base, fname = os.path.split(new_json_file)
    if not os.path.exists(base):
        os.makedirs(base)
    with open(new_json_file, 'w') as f:
        f.write(json.dumps(new_annos))
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")
def write_txt_file(list_infos, filepath):
    basedir, filename = os.path.split(filepath)
    os.makedirs(basedir, exist_ok=True)
    with open(filepath, 'w') as f:
        for info in list_infos:
            f.write(str(info) + '\n')
    print(f'Finish write {len(list_infos)} infos into {filepath}.')

