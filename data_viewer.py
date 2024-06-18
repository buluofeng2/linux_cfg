import json
from matplotlib import pyplot as plt
import os
import random
import cv2
def dump_into_file(new_annos, new_json_file):
    with open(new_json_file, 'w') as f:
        for anno in new_annos:
            f.write(json.dumps(anno) + '\n')
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")
def read_json_file(json_file):
    res = []
    with open(json_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            jd =json.loads(line.strip())
            res.append(jd)
    return res
def read_json_filev2(json_file):
    jds = []
    with open(json_file, 'r') as f:
        jds = json.load(f)
    return jds

import cv2
import random
def view_anno(jd):
    fn = jd['filename']
    inss = jd['instances']
    fp = os.path.join('/mnt/lustre/irdc_rd/HKCustoms/images', fn)
    plt.figure(figsize=(10, 20))
    ax = plt.subplot(1, 1, 1)  # 用ax接收当前子图对象
    I = cv2.imread(fp)
    for ins in inss:
        bbox = ins['bbox']
        score = ins['score']
        if score < 0.2:
            continue
        x1, y1, x2, y2 = bbox
        # 实例化矩形对象:设置边框的宽度，边框的颜色，填充颜色
        rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, alpha=0.8, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)  # 在已有的图片上添加其他对象
        plt.text(x1, y1, '%.2f'%(score), color='r', ha='left')
    ax.imshow(I)  # 显示图片
    plt.show()
n = random.randint(0, len(unsup_jsons) - 1)
view_anno(unsup_jsons[5])
