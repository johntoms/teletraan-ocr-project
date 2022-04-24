# 简单的图片文字识别系统
> 本系统采用 `muggle-ocr` 包进行图片文字识别，目前仅支持系统训练好的两种模块。

## 架构
- flask
- Vue(CDN)
- mysql
- docker
- muggle-ocr


## 容器
```text
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
```

## 使用文档
### 启动容器
```bash
docker run --name flask-muggle-ocr \
    -p 5000:5000 \
    -d registry.cn-hangzhou.aliyuncs.com/public_app/flask-muggle-ocr:latest
```

### 前端地址
```text
# 访问 http://<host>:<port>
# 默认选择验证码识别类型
1. 选择图片的识别类型
2. 点击 `选取文件`
3. 点击 `开始识别`
注意事项: 只能上传jpg/png/jpeg文件，且不超过1MB
```

### 后端使用 API 进行验证
```python
import requests
host = '127.0.0.1'
port = 5000
# model_type 识别方法 options
# captcha       :      验证码识别
# ocr           :      文字识别

data = {
    'model_type': 'captcha'
}
files = {'file': open('captcha001.jpg', 'rb')}
res = requests.post('http://{}:{}/api/v1/muggle-ocr'.format(host, port), data=data,
                    files=files)
print(res.text)
print(res.json())
```
