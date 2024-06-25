- `docker run --name test --gpus all --mount type=bind,source=D:\code\faceswap,target=/data -idt faceswap:latest`
- `docker exec -it test /bin/bash`
- `docker container stop test`
- `docker container rm test`
-----
- `docker cp /home/b/miniconda3/envs/yolo1.7 test:/opt/conda/envs`
- `docker commit -a 'author' -m 'instruction' <container_name> <image_name>`
- `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package`

# extract image
- `python faceswap.py extract -i /data/src/xue.mp4 -o /data/src/faces_xue/`
- `python faceswap.py extract -i /data/src/wandon.mp4 -o /data/src/faces_wandon/`
- `python faceswap.py extract -i /data/src/by.mp4 -o /data/src/faces_by/`

# training
- `python faceswap.py train -A /data/src/faces_xue/ -B /data/src/faces_wandon/ -m /data/mn_model/`

# convert
- `python faceswap.py convert -i /data/src/xue.mp4 -o /data/dst/converted/c_xue -m /data/mn_model/`

# generate a video
- `ffmpeg -i /data/dst/converted/c_xue/xue_%0d.png -c:v libx264 -vf "fps=25,format=yuv420p" /data/dst/converted/c_xue.mp4`
