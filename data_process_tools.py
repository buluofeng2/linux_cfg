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

# write all anno into 1 line.
def dump_into_file(new_annos, new_json_file):
    base, fname = os.path.split(new_json_file)
    if not os.path.exists(base):
        os.makedirs(base)
    with open(new_json_file, 'w') as f:
        f.write(json.dumps(new_annos))
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")

# each json in the new_annos list will be write into 1 line.
def dump_into_file(new_annos, new_json_file):
    base, fname = os.path.split(new_json_file)
    if not os.path.exists(base):
        os.makedirs(base)
    with open(new_json_file, 'w') as f:
        for anno in new_annos:
            f.write(json.dumps(anno) + '\n')
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")

# write the json into more pretty format
def dump_into_file(new_annos, new_json_file):
    base, fname = os.path.split(new_json_file)
    if not os.path.exists(base):
        os.makedirs(base)
    with open(new_json_file, 'w') as f:
        f.write(json.dumps(new_annos, indent=4))
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")

def write_txt_file(list_infos, filepath):
    basedir, filename = os.path.split(filepath)
    os.makedirs(basedir, exist_ok=True)
    with open(filepath, 'w') as f:
        for info in list_infos:
            f.write(str(info) + '\n')
    print(f'Finish write {len(list_infos)} infos into {filepath}.')


# copy file
import shutil
def copyfile(src_path, dst_path):
    assert os.path.exists(src_path), src_path
    base, filename = os.path.split(dst_path)
    os.makedirs(base, exist_ok=True)
    shutil.copy(src_path, dst_path)
    # shutil.copy(src_path, dst_path)  # keep metadata for src file.
# 遍历文件夹
for dirpath, dirnames, filenames in os.walk(img_dir):
    for finename in filenames:
        if finename.endswith('.jpg'):
            abs_p = os.path.join(dirpath, filename)
