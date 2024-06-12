import json
import os
import matplotlib.pyplot as plt
import random
import cv2
import numpy as np


all_suitcase_json = [
    '/mnt/lustre/songfaxing/code/HKCustoms/UP/experiments/hkc_20240509/train_all+20240303_suitcase.json',
    '/mnt/lustre/songfaxing/code/HKCustoms/UP/experiments/hkc_20240509/20240515_vertical_cam_suitcase.json',
    # '/mnt/lustre/songfaxing/code/HKCustoms/UP/experiments/hkc_20240509/20240418_test_images_suitcase.json'
]
crop_jsons = [
    '/mnt/lustre/irdc_rd/HKCustoms/images/ips_crop_images_v2/ips_det_json/train_all+20240303_suitcase_ips3x.json',
    '/mnt/lustre/irdc_rd/HKCustoms/images/ips_crop_images_v2/ips_det_json/20240515_vertical_cam_suitcase_ips3x.json',
    # '/mnt/lustre/irdc_rd/HKCustoms/images/ips_crop_images_v2/ips_det_json/20240418_test_images_suitcase_ips3x.json'
]
crop_dir = '/mnt/lustre/irdc_rd/HKCustoms/images/ips_crop_images_v2/'
img_dir = '/mnt/lustre/irdc_rd/HKCustoms/images/'

# file op
def read_json_file(json_file):
    res = []
    with open(json_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            jd =json.loads(line.strip())
            res.append(jd)
    return res
def dump_into_file(new_annos, new_json_file):
    basedir, filename = os.path.split(new_json_file)
    os.makedirs(basedir, exist_ok=True)
    with open(new_json_file, 'w') as f:
        for anno in new_annos:
            f.write(json.dumps(anno) + '\n')
    print(f"Write {len(new_annos)} annotations into {new_json_file}.")
def get_new_img_path(img_path, idx):
    img_path_n = img_path.replace(img_dir, crop_dir)
    basename, ext = os.path.splitext(img_path_n)
    crop_img_path = basename + f'_{str(idx)}' + ext
    return crop_img_path
def save_img(output_img, img_path):
    basedir, name = os.path.split(img_path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    cv2.imwrite(img_path, output_img)

def crop_image_with_bbox_for_ips(img, bbox, borders, crop_img_path):
    """
        img: cv2.imread get the image file, [H, W, C]
        bbox: x1, y1, x2, y2
        borders: left, top, right, bottom 外扩多少像素
        crop_img_path: the path for the crop image.
    """
    x1, y1, x2, y2 = bbox
    l, t, r, b = borders
    nx1, ny1, nx2, ny2 = x1 - l, y1 - t, x2 + r, y2 + b
    output_img = img[ny1:ny2, nx1:nx2, :]
    # output_img = img[y1:y2, x1:x2, :]
    save_img(output_img, crop_img_path)

def transform_bbox(bbox, borders):
    x1, y1, x2, y2 = bbox
    l, t, r, b = borders
    nx1, ny1, nx2, ny2 = l, t, x2 - x1 + l, y2 - y1 + t
    w, h = l + r + x2 - x1, t + b + y2 - y1
    return [nx1, ny1, nx2, ny2], w, h

def get_new_anno(crop_img_path, bbox, borders):
    filename = crop_img_path.replace(img_dir, '')
    nbbox, image_width, image_height = transform_bbox(bbox, borders)
    instances = [{'label': 1, 'is_ignored': False, 'bbox': nbbox}]
    anno = {
        'filename': filename,
        'image_width': image_width,
        'image_height': image_height,
        'instances':instances
    }
    return anno

def get_random_border(min_x, max_x, M):
    min_y = min(min_x, M)
    max_y = min(max_x, M)
    return random.randint(min_y, max_y)

def get_borders(bbox, width, height, ratio=0.5, min_ratio=0.1):
    x1, y1, x2, y2 = bbox
    L, T, R, B = x1, y1, width - x2, height - y2
    W, H = x2 - x1, y2 - y1
    random_int = random.randint(1, 100)  # 生成 1 到 100 之间的随机整数
    l = get_random_border(int(W * min_ratio), int(W * ratio), L)
    r = get_random_border(int(W * min_ratio), int(W * ratio), R)    
    t = get_random_border(int(H * min_ratio), int(H * ratio), T)     
    b = get_random_border(int(H * min_ratio), int(H * ratio), B)        
    return [l, t, r, b]

def get_all_bboxes(instances):
    bboxes = []
    for ins in instances:
        bboxes.append(ins['bbox'])
    return bboxes

def scale_bbox(bbox, border):
    x1 ,y1 ,x2 ,y2 = bbox
    l, t, r, b = border
    return [x1 - l, y1 - t, x2 + r, y2 + b]

def IoU(bboxes, bbox):
    boxes1 = np.array(bboxes)
    boxes2 = np.array([bbox])
    # 计算交集区域的坐标
    x_left = np.maximum(boxes1[:, 0], boxes2[:, 0])
    y_top = np.maximum(boxes1[:, 1], boxes2[:, 1])
    x_right = np.minimum(boxes1[:, 2], boxes2[:, 2])
    y_bottom = np.minimum(boxes1[:, 3], boxes2[:, 3])

    # 计算交集区域的面积
    inter_width = np.maximum(0, x_right - x_left)
    inter_height = np.maximum(0, y_bottom - y_top)
    inter_area = inter_width * inter_height

    # 计算每个矩形框的面积
    boxes1_area = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    # boxes2_area = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])

    # # 计算并集区域的面积
    # union_area = boxes1_area + boxes2_area - inter_area

    # # 计算IoU
    # iou = inter_area / union_area
    iof = inter_area / boxes1_area
    return iof

def bbox_collision_detection(bboxes, new_bbox, bbox_idx, collision_thr=0.5):
    if len(bboxes) == 1:
        return False
    rest_bboxes = [b for idx, b in enumerate(bboxes) if idx != bbox_idx]
    iof = IoU(rest_bboxes, new_bbox)
    collision_flag = np.any(iof >= collision_thr)
    return collision_flag

for src_json, dst_json in zip(all_suitcase_json, crop_jsons):
    src_annos = read_json_file(src_json)
    new_annos = []
    for anno in src_annos:
        instances = anno['instances']
        bboxes = get_all_bboxes(instances)
        width, height = anno['image_width'], anno['image_height']
        filename = anno['filename']
        img_path = os.path.join(img_dir, filename)
        image = cv2.imread(img_path)
        for idx, ins in enumerate(instances):
            if ins['is_ignored']:
                continue
            bbox = [int(a) for a in ins['bbox']]
            scale_ratio = 1.0
            scale_cnt = 0
            while scale_cnt < 5:
                borders = get_borders(bbox, width, height, ratio=scale_ratio, min_ratio=0.02)
                crop_img_path = get_new_img_path(img_path, idx)
                anno = get_new_anno(crop_img_path, bbox, borders)
                new_box = scale_bbox(bbox, borders)
                collision_flag = bbox_collision_detection(bboxes, new_box, idx, collision_thr=0.25)
                scale_cnt += 1
                scale_ratio = 0.9 * scale_ratio
                if collision_flag:
                    continue
                else:
                    break
            if collision_flag:
                continue
            new_annos.append(anno)
            # crop image
            crop_image_with_bbox_for_ips(image, bbox, borders, crop_img_path)
    dump_into_file(new_annos, dst_json)
