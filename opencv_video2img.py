# -*- coding:utf8 -*-
import cv2
import os
import shutil
from pathlib import Path
 
def get_frame_from_video(video_name, interval=125, save_dir=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    # read the video
    video_capture = cv2.VideoCapture(video_name)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    j = 0
    out_frames = int(total_frames / interval) + 1
    for i in range(out_frames):
        j = i * interval
        if j >= total_frames:
            continue
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, j)
        success, frame = video_capture.read()
        if not success:
            print(f"Error: Could not read frame {j} from {video_name}.")
            continue
        img_name = f'img_{str(i)}_frame{str(j)}.jpg'
        save_path = os.path.join(save_dir, img_name)
        cv2.imwrite(save_path, frame)
    return out_frames

def get_video_infos(video_path):
    cap = cv2.VideoCapture(video_path)

    total_frames = 0
    # 检查视频是否打开成功
    if not cap.isOpened():
        print(f'Error: Could not open video{video_path}.')
    else:
        # 获取视频的总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 获取视频的频率
        fps = cap.get(cv2.CAP_PROP_FPS)

        print(f'Video Path: {video_path}')
        print(f"\tTotal frames: {total_frames}")
        print(f"\tFPS         : {fps}")

    # 释放视频捕获对象
    cap.release()
    return total_frames

def get_all_videos(video_dir):
    total_frames = 0
    if not os.path.exists(video_dir):
        print(f'Error: No such file or dir :{video_dir}.')
    pwd = Path(video_dir)
    for video_path in pwd.rglob('*'):
        suffix = video_path.suffix
        if suffix != '.mkv':
            continue
        if suffix not in ['.MP4', '.mp4', '.avi', '.MOV', '.mkv']:# 后缀格式添加到后面的列表里
            continue
        video_name = video_path.resolve().name.replace(suffix, '').replace(' ', '-')
        parents = str(video_path.resolve().parent).replace(str(pwd),'').lstrip("/")

        frame = get_video_infos(str(video_path.resolve()))
        total_frames += frame
    print('All Frames Number:', total_frames)

def loop_all_videos(video_dir, img_save_dir):
    img_save_dir = Path(img_save_dir)
    total_frames = 0
    if not os.path.exists(video_dir):
        print(f'Error: No such file or dir :{video_dir}.')
    pwd = Path(video_dir)
    for video_path in pwd.rglob('*'):
        suffix = video_path.suffix
        if suffix != '.mkv':
            continue
        if suffix not in ['.MP4', '.mp4', '.avi', '.MOV', '.mkv']:# 后缀格式添加到后面的列表里
            continue
        video_name = video_path.resolve().name.replace(suffix, '').replace(' ', '-')
        parents = str(video_path.resolve().parent).replace(str(pwd),'').lstrip("/")

        save_dir = (img_save_dir / parents / video_name).resolve()
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = str(save_dir)

        # exec the loop func
        extract_frames = get_frame_from_video(str(video_path.resolve()), interval=125, save_dir=save_path)
        total_frames += extract_frames
        print(f'Extracted {extract_frames} frames from video {str(video_path.resolve())}.')
    print('All Extracted Frames Number:', total_frames)

if __name__ == '__main__':
    # # 视频文件名字
    # video_name = '/mnt/lustrenew/songfaxing/HKC/t2_data_20240604/Export_6-4-2024/Cam_11154C-L5_Carrousel_14_and_15/5_3_2024 4_29_59 PM (UTC+08_00).mkv'
    # frames = get_video_infos(video_name)

    video_dir = '/mnt/lustrenew/songfaxing/HKC/t2_data_20240604/Export_6-4-2024/'
    img_save_dir = '/mnt/lustrenew/songfaxing/HKC/images/Export_6-4-2024'
    # get_all_videos(video_dir)  # total frame: 1037760
    loop_all_videos(video_dir, img_save_dir, )
    
