FROM python:3.9.6
LABEL Author="caoxiangpeng"
ADD requirements.txt /usr/src
RUN \
    # 替换国内源
    apt-get update \
    && apt-get install libgl1-mesa-glx gcc ffmpeg libsm6 libxext6 -y \
    && rm -rf /var/cache/apt/* \
    && pip install  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com  -r /usr/src/requirements.txt

# 保留此系统的编译能力，为以后安装做基础
ADD . /code
WORKDIR /code
EXPOSE 5000/tcp
CMD ["/bin/sh", "start.sh"]