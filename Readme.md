# 简单的图片文字识别系统
> 本系统采用 `muggle-ocr` 包进行图片文字识别，目前仅支持系统训练好的两种模块。

## 架构
- flask
- Vue(CDN)
- mysql
- docker
- muggle-ocr
## 项目主要配置
```text
1. 图片存储位置: /code/muggle-images
2. 日志(默认)存储位置: /tmp/app.log
3. 上传大小配置: muggle-ocr 环境变量 `MAX_CONTENT_LENGTH`
```

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
> 服务器要求：建议 `2H4G` .
### `docker` 部署
```shell
# 部署 teletraan-muggle-ocr
docker run --name teletraan-muggle-ocr \
    -p 5000:5000 \
    -e FLASK_ENV='development' \
    -e LANG='en_US.UTF-8' \
    -e LC_CTYPE='en_US.UTF-8' \
    -e APP_TIMEZONE='UTC' \
    -e DATABASE_HOST='teletraan-mysql' \
    -e DATABASE_PORT=3306 \
    -e DATABASE_USER='teletraan' \
    -e DATABASE_NAME='teletraan' \
    -e DATABASE_PASSWORD='Teletraan-OCR@1024' \
    -d registry.cn-hangzhou.aliyuncs.com/private_app/teletraan-ocr-project:1.0.3


# 部署 mysql
docker run --name teletraan-mysql \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD='56tP3!U8NEa$DYwT' \
    -e MYSQL_DATABASE='teletraan' \
    -e MYSQL_USER='teletraan' \
    -e MYSQL_PASSWORD='Teletraan-OCR@1024' \
    -v E:\tmp\tmp_docker_docker:/var/lib/mysql \
    -d mysql:5.7.37 \
    --max_connections=1000 \
    --character-set-server=utf8mb4 \
    --collation-server=utf8mb4_general_ci \
    --default-authentication-plugin=mysql_native_password


# 初始化数据库
docker exec teletraan-muggle-ocr python manage.py db upgrade
```
### `docker-compose` 部署（推荐）
```text
# 修改密码 和 mysql 本地文件存储
------------------------------------------------
## docker-compose.yml
version: '3'
services:
  mysql:
    image: mysql:5.7.37
    restart: always
    container_name: teletraan-mysql
    environment:
      MYSQL_ROOT_PASSWORD: '56tP3!U8NEa$DYwT' # 建议修改
      MYSQL_DATABASE: teletraan
      MYSQL_USER: teletraan
      MYSQL_PASSWORD: Teletraan-OCR@1024 # 建议修改
    ports:
      - 3307:3306
    networks:
      - ocr
    volumes:
      - your_customer_mysql_dir:/var/lib/mysql  # 建议配置，如确实不需要可以删除
    command:
      --max_connections=1000
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --default-authentication-plugin=mysql_native_password
  muggle-ocr:
    image: registry.cn-hangzhou.aliyuncs.com/private_app/teletraan-ocr-project:1.0.3
    restart: always
    container_name: teletraan-muggle-ocr
    environment:
      FLASK_ENV: development
      LANG: en_US.UTF-8
      LC_CTYPE: en_US.UTF-8
      APP_TIMEZONE: UTC
      DATABASE_HOST: mysql
      DATABASE_PORT: 3306
      DATABASE_USER: teletraan
      DATABASE_NAME: teletraan
      DATABASE_PASSWORD: Teletraan-OCR@1024 # 同上
    ports:
      - 5000:5000
    networks:
      - ocr
    depends_on:
      - mysql

networks:
  ocr: {}
---------------------------------------------------
# ** docker-compose 启动后，不要忘记了执行数据迁移呦 **

# 启动
docker-compose -f docker-compose.yml up -d

# 迁移数据库
docker exec teletraan-muggle-ocr python manage.py db upgrade

# 停止
docker-compose -f docker-compose.yml stop
# 删除
docker-compose -f docker-compose.yml rm
```

### 前端地址
```text
# 访问 http://<host>:<port>/ocr/index
# 默认选择验证码识别类型
1. 选择图片的识别类型
2. 点击 `选取文件`
3. 点击 `开始识别`
注意事项: 只能上传jpg/png/jpeg文件，且不超过10MB
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
files = {'file': open('test02.jpg', 'rb')}
res = requests.post('http://{}:{}/ocr/api/v1/muggle-ocr'.format(host, port), data=data,
                    files=files)
print(res.text)
```
