docker run --name test --gpus all --mount type=bind,source=D:\code\faceswap,target=/data -idt faceswap:latest
docker exec -it test /bin/bash
docker container stop test
docker container rm test

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

# extract image
python faceswap.py extract -i /data/src/douyin.mp4 -o /data/src/faces/
python faceswap.py extract -i /data/src/by.mp4 -o /data/src/faces_by/

# training
python faceswap.py train -A /data/src/faces/ -B /data/src/faces_by/ -m /data/mn_model/

# convert
python faceswap.py convert -i /data/src/douyin.mp4 -o /data/dst/converted/c_douyin.mp4 -m /data/mn_model/
